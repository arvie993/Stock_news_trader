import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from dotenv import load_dotenv

load_dotenv()

# Hot stocks to monitor - Add or remove as needed
STOCKS = [
    # Mega-cap Tech
    {"symbol": "TSLA", "name": "Tesla Inc"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation"},
    {"symbol": "AAPL", "name": "Apple Inc"},
    {"symbol": "MSFT", "name": "Microsoft Corporation"},
    {"symbol": "GOOGL", "name": "Alphabet Inc"},
    {"symbol": "AMZN", "name": "Amazon.com Inc"},
    {"symbol": "META", "name": "Meta Platforms Inc"},
    
    # Semiconductor & Chip Makers
    {"symbol": "AMD", "name": "Advanced Micro Devices"},
    {"symbol": "INTC", "name": "Intel Corporation"},
    {"symbol": "MU", "name": "Micron Technology"},
    
    # Finance & Crypto
    {"symbol": "COIN", "name": "Coinbase Global Inc"},
    {"symbol": "V", "name": "Visa Inc"},
    {"symbol": "MA", "name": "Mastercard Inc"},
    
    # AI & Growth Stocks
    {"symbol": "PLTR", "name": "Palantir Technologies"},
    {"symbol": "MSTR", "name": "MicroStrategy Inc"},
    {"symbol": "MRVL", "name": "Marvell Technology"},
]

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# API Keys - Loaded from .env file
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Email settings
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")


def send_email(subject, body):
    """Send an email notification."""
    print(f"  📧 Attempting to send email...")
    print(f"  From: {EMAIL_ADDRESS}")
    print(f"  To: {EMAIL_TO}")
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("  🔐 Logging in to Gmail...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("  📤 Sending email...")
            server.sendmail(EMAIL_ADDRESS, EMAIL_TO, msg.as_string())
        print("  ✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"  ❌ Failed to send email: {e}")
        return False

def check_stock(stock_symbol, company_name):
    """Check a single stock for significant price changes and send alerts if needed."""
    print(f"\n📊 Checking {stock_symbol} ({company_name})...")
    
    # Get stock data from Alpha Vantage
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        data = response.json()
        
        if "Time Series (Daily)" not in data:
            print(f"  ⚠️ Could not get data for {stock_symbol}: {data.get('Note', data.get('Error Message', 'Unknown error'))}")
            return
        
        data = data["Time Series (Daily)"]

        # Get yesterday's closing stock price
        data_list = [value for (key, value) in data.items()]
        yesterday_data = data_list[0]
        yesterday_closing_price = float(yesterday_data["4. close"])

        # Get the day before yesterday's closing stock price
        day_before_yesterday_data = data_list[1]
        day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

        # Find the positive difference
        difference = yesterday_closing_price - day_before_yesterday_closing_price
        positive_difference = abs(difference)

        # Work out the percentage difference in price
        percentage_difference = (positive_difference / day_before_yesterday_closing_price) * 100

        # Determine if price went up or down for the emoji
        up_down = "🔺" if difference > 0 else "🔻"

        print(f"  Price: ${yesterday_closing_price:.2f} ({up_down}{percentage_difference:.2f}%)")

        # If percentage is greater than 5 then get news
        if percentage_difference > 5:
            print(f"  🚨 Significant change detected! Fetching news...")
            
            news_params = {
                "q": company_name,
                "apiKey": NEWS_API_KEY,
            }
            
            news_response = requests.get(NEWS_ENDPOINT, params=news_params)
            articles = news_response.json().get("articles", [])
            
            if not articles:
                print(f"  No news articles found for {company_name}")
                return
            
            # Get first 3 articles
            first_three_articles = articles[:3]
            
            # Format articles for email
            email_body = f"{stock_symbol}: {up_down}{round(percentage_difference)}%\n"
            email_body += f"Price: ${yesterday_closing_price:.2f}\n"
            email_body += "=" * 50 + "\n\n"
            
            for i, article in enumerate(first_three_articles, 1):
                email_body += f"📰 Article {i}:\n"
                email_body += f"Headline: {article['title']}\n"
                email_body += f"Brief: {article['description']}\n"
                email_body += f"Link: {article.get('url', 'N/A')}\n\n"
            
            # Send email
            subject = f"🚨 {stock_symbol} Stock Alert: {up_down}{round(percentage_difference)}%"
            if send_email(subject, email_body):
                print(f"  ✅ Email sent!")
        else:
            print(f"  ✓ No significant change (threshold: 5%)")
            
    except Exception as e:
        print(f"  ❌ Error checking {stock_symbol}: {e}")


# Main execution - check all stocks
print("=" * 50)
print("🔍 STOCK PRICE MONITOR")
print("=" * 50)

for i, stock in enumerate(STOCKS):
    check_stock(stock["symbol"], stock["name"])
    # Alpha Vantage free tier: 5 calls/minute, so wait 15 seconds between calls
    if i < len(STOCKS) - 1:
        print("  ⏳ Waiting 15 seconds (API rate limit)...")
        time.sleep(15)

print("\n" + "=" * 50)
print("✅ Monitoring complete!")
print("=" * 50)

