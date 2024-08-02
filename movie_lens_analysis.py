#import necessary libraries
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, avg
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Spark session
logger.info("Initializing Spark session...")
spark = SparkSession.builder \
    .appName("MovieLensAnalysis") \
    .getOrCreate()
logger.info("Spark session initialized.")

try:
    # Load data from S3
    logger.info("Loading data...")
    movies = spark.read.csv("s3://movielens-gfk/datasets/movies.dat", sep="::", inferSchema=True, header=False).toDF("movie_id", "title", "genres")
    ratings = spark.read.csv("s3://movielens-gfk/datasets/ratings.dat", sep="::", inferSchema=True, header=False).toDF("user_id", "movie_id", "rating", "timestamp")
    users = spark.read.csv("s3://movielens-gfk/datasets/users.dat", sep="::", inferSchema=True, header=False).toDF("user_id", "gender", "age", "occupation", "zip_code")
    logger.info("Data loaded successfully.")

    # Filter users aged 18-49
    logger.info("Filtering users aged 18-49...")
    filtered_users = users.filter((col("age") >= 18) & (col("age") <= 49))
    logger.info("Users filtered.")

    # Join ratings with filtered users
    logger.info("Joining ratings with filtered users...")
    filtered_ratings = ratings.join(filtered_users, "user_id")
    logger.info("Ratings joined with filtered users.")

    # Extract year from title and filter movies released after 1989
    logger.info("Extracting year from titles and filtering movies...")
    movies = movies.withColumn("year", split(col("title"), "\\(").getItem(1).substr(0, 4).cast("int"))
    filtered_movies = movies.filter(col("year") > 1989)
    logger.info("Movies filtered.")

    # Explode genres
    logger.info("Exploding genres...")
    movies_with_genres = filtered_movies.withColumn("genre", explode(split(col("genres"), "\\|")))
    logger.info("Genres exploded.")

    # Join ratings with movies
    logger.info("Joining ratings with movies...")
    ratings_with_movies = filtered_ratings.join(movies_with_genres, "movie_id")
    logger.info("Ratings joined with movies.")

    # Calculate average ratings per genre and year
    logger.info("Calculating average ratings per genre and year...")
    average_ratings = ratings_with_movies.groupBy("genre", "year").agg(avg("rating").alias("average_rating"))
    logger.info("Average ratings calculated.")

    # Save results to S3
    output_path = "s3://movielens-gfk/output/"
    logger.info("Writing results to S3...")
    average_ratings.write.csv(output_path, header=True, mode="overwrite")
    logger.info(f"Results written to {output_path}.")

except Exception as e:
    logger.error("An error occurred", exc_info=True)
finally:
    # Stop the Spark session
    logger.info("Stopping Spark session...")
    spark.stop()
    logger.info("Spark session stopped.")
