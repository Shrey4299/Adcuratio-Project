from decouple import config


DATABASE_URI = config(
    "DATABASE_URI", default="postgresql://shrey:Sonu619@localhost:5432/Ecommerce"
)