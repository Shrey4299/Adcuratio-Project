from typing import Annotated
import nltk
import requests
from bs4 import BeautifulSoup
from fastapi import (APIRouter, Depends, Header, HTTPException, Query, Request,
                     status)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from starlette.responses import JSONResponse

from src.auth.token_access import verify_token
from src.common.helper import (create_description_word_count,
                               create_generalised_description,
                               extract_post_data, fetch_content)
from src.database.connection import Session
from src.database.models import WebscrapResponse
from src.database.schema import (GeneralisedDescription, GeneralisedWordCount, User,
                                 WebScraper)

hacker_news_router = APIRouter(tags=["hacker news api"], prefix="/hackernews")


@hacker_news_router.get("/", response_model=WebscrapResponse)
async def get_hacker_news_data(
    current_user: Annotated[User, Depends(verify_token)]
) -> JSONResponse:
    """
    Retrieve a webscrap.

    Query Param:
    - None

    Parameters:
    - None

    Returns:
      - 200 OK: List of users.
      - 404 : WebScrap not found.
    """

    session = Session()
    query = session.query(WebScraper)

    webscrapers = query.all()

    if webscrapers:
        webscrapers_list = []
        for webscrap in webscrapers:
            webscraper_dict = {
                "id": webscrap.id,
                "description": webscrap.description,
                "image": webscrap.image,
                "titles": webscrap.titles,
                "url": webscrap.url,
            }
            webscrapers_list.append(webscraper_dict)

        response = WebscrapResponse(
            success=True,
            message="Web Scrap found",
            data=webscrapers_list,
            status_code=status.HTTP_200_OK,
        )

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="web scrap not found"
        )


@hacker_news_router.post("/", response_model=WebscrapResponse)
async def create_hacker_news_entries(
    n: int = Query(..., gt=0), current_user: User = Depends(verify_token)
) -> JSONResponse:

    """
    Scrape and create new web scraping entries.

    Query Parameters:
    - `n`: Number of pages to scrape.

    Returns:
    - 200 OK: Successfully scraped and created web scraping entries.
    """

    all_post_data = []

    url = "https://thehackernews.com/"

    for _ in range(n):
        soup = fetch_content(url)
        post_data = extract_post_data(soup)
        all_post_data.extend(post_data)

        next_page_url = soup.find(class_="blog-pager-older-link-mobile")["href"]

        url = next_page_url

    session = Session()
    for data in all_post_data:
        # Create WebScraper entry
        new_entry = WebScraper(
            description=data["description"],
            image=data["image_source"],
            titles=data["title"],
            url=data["url"],
        )

        session.add(new_entry)
        session.flush()  # Flush to get the ID before committing

        # Create GeneralisedDescription entry
        generalised_description = create_generalised_description(data["description"])
        generalised_entry = GeneralisedDescription(
            description=generalised_description, web_scraper=new_entry
        )
        session.add(generalised_entry)
        session.flush()  # Flush to get the ID before committing

        generalised_description_words = create_description_word_count(
            generalised_description
        )
        print(generalised_description_words)
        print(type(generalised_description_words))

        import json

        sample = json.dumps(generalised_description_words)

        word_count_entry = GeneralisedWordCount(
            word_count_desc=sample,
            generalised_description=generalised_entry,
        )

        session.add(word_count_entry)
        session.flush()  # Flush to get the ID before committing

    session.commit()
    session.close()

    response = WebscrapResponse(
        success=True,
        message=f"{len(all_post_data)} web scraping entries created",
        data=None,
        status_code=status.HTTP_200_OK,
    )

    return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)


@hacker_news_router.get("/search/", response_model=WebscrapResponse)
async def search_links_by_keyword(
    keyword: str = Query(..., title="Keyword to search"),
    current_user: User = Depends(verify_token),
) -> JSONResponse:
    """
    Search links in the database by keyword.

    Query Parameters:
    - `keyword`: Keyword to search in the descriptions.

    Returns:
    - List of links whose description contains the keyword.
    """

    try:
        session = Session()

        links = (
            session.query(WebScraper)
            .filter(WebScraper.description.ilike(f"%{keyword}%"))
            .all()
        )

        if not links:
            raise HTTPException(
                status_code=404, detail="No links found with the given keyword"
            )

        url_list = [{"url": link.url} for link in links]

        response = WebscrapResponse(
            success=True,
            message="Links found",
            data=url_list,
            status_code=status.HTTP_200_OK,
        )

        return JSONResponse(content=response.dict(), status_code=status.HTTP_200_OK)

    except Exception as e:
        response = WebscrapResponse(
            success=False,
            message=f"An error occurred: {str(e)}",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return JSONResponse(
            content=response.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    finally:
        session.close()
