# Stock Price Monitor 📈

A Python automation tool that monitors stock price changes and sends email alerts when significant price movements occur, along with relevant news articles.

## Features 🚀

- **Real-time Stock Monitoring**: Tracks 15+ popular stocks daily
- **Price Change Detection**: Alerts when stocks move >5% day-over-day
- **News Integration**: Fetches top 3 relevant news articles for each alert
- **Email Notifications**: Receives formatted email summaries with headlines and links
- **Automated Scheduling**: Runs automatically via Windows Task Scheduler
- **Rate-Limited API Calls**: Respects free tier API rate limits
- **Secure Credentials**: Stores API keys in `.env` file (not in code)

## Monitored Stocks 📊

| Category | Stocks |
|----------|--------|
| **Mega-cap Tech** | TSLA, NVDA, AAPL, MSFT, GOOGL, AMZN, META |
| **Semiconductors** | AMD, INTC, MU |
| **Finance & Crypto** | COIN, V, MA |
| **AI & Growth** | PLTR, MSTR, MRVL |

## Prerequisites 📋

- Python 3.8+
- Windows OS (for Task Scheduler)
- Gmail account with 2-Step Verification enabled
- Internet connection

## Installation 🛠️

### 1. Clone/Download the Project
```bash
cd Day36-StockTradingNews/stock-news-normal-start
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install requests python-dotenv
```

## Configuration ⚙️

### 1. Get API Keys

**Alpha Vantage** (Stock Data)
- Visit: https://www.alphavantage.co/support/#api-key
- Fill in your details
- Receive API key via email
- Free tier: 25 calls/day

**News API** (News Articles)
- Visit: https://newsapi.org/register
- Create account with email
- Verify email
- Copy API key from dashboard
- Free tier: 100 requests/day

**Gmail App Password** (Email Alerts)
- Go to: https://myaccount.google.com/security
- Enable 2-Step Verification (if not already)
- Go to **App passwords**
- Generate password for "Mail" on "Windows Computer"
- Use the 16-character password (spaces removed)

### 2. Create `.env` File

Create a file named `.env` in the project directory:

```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
EMAIL_TO=your_email@gmail.com
```

**⚠️ Important**: Never commit `.env` to git. Add it to `.gitignore`:
```
.env
__pycache__/
*.pyc
```

## Usage 🎯

### Manual Run
```bash
python main.py
```

Output example:
```
==================================================
🔍 STOCK PRICE MONITOR
==================================================

📊 Checking TSLA (Tesla Inc)...
  Price: $438.07 (🔻2.59%)
  ✓ No significant change (threshold: 5%)

📊 Checking PLTR (Palantir Technologies)...
  Price: $167.86 (🔻5.56%)
  🚨 Significant change detected! Fetching news...
  📧 Attempting to send email...
  ✅ Email sent!

⏳ Waiting 15 seconds (API rate limit)...

==================================================
✅ Monitoring complete!
==================================================
```

### Automated Scheduling (Windows Task Scheduler)

#### Step 1: Open Task Scheduler
Press `Win + R` → type `taskschd.msc` → Enter

#### Step 2: Create Basic Task
1. Right-click **Task Scheduler Library** → **Create Basic Task**
2. **Name**: `Stock Price Monitor`
3. **Description**: Checks stocks for significant price changes and sends alerts
4. Click **Next**

#### Step 3: Set Trigger
1. Select **Daily** → **Next**
2. Set **Time**: 9:30 AM (market open) or your preferred time
3. Click **Next**

#### Step 4: Set Action
1. Select **Start a program** → **Next**
2. **Program/script**: `C:\venv\rain\Scripts\python.exe` (or your Python path)
3. **Add arguments**: `main.py`
4. **Start in**: Full path to project folder:
   ```
   C:\Users\YourUsername\OneDrive - Microsoft\All demos\100_days_of_python\Day36-StockTradingNews\stock-news-normal-start
   ```
5. Click **Next** → **Finish**

#### Step 5: Configure Task Properties
1. Right-click the task → **Properties**
2. **General** tab: Check **Run with highest privileges**
3. Click **OK**

#### Testing the Task
1. Right-click **Stock Price Monitor** → **Run**
2. Check your email within 2-3 minutes
3. Verify console output in Task Scheduler History

### Add Multiple Run Times
To run at 9:30 AM, 12:30 PM, and 3:30 PM:
1. Right-click task → **Properties**
2. **Triggers** tab → **New...**
3. Add another daily trigger at different time
4. Repeat for each desired time
5. Click **OK**

## How It Works 🔧

### Daily Workflow

1. **Fetch Stock Data** (Alpha Vantage)
   - Gets yesterday's closing price
   - Gets day-before-yesterday's closing price
   - Calculates percentage change

2. **Check Threshold**
   - If change > 5%: Continue
   - If change ≤ 5%: Skip to next stock

3. **Fetch News** (News API)
   - Searches for articles about the company
   - Retrieves top 3 results

4. **Send Alert** (Gmail SMTP)
   - Formats email with:
     - Stock symbol & percentage change (🔺 up, 🔻 down)
     - Current price
     - 3 news article headlines, briefs, and links
   - Sends via Gmail

5. **Rate Limiting**
   - Waits 15 seconds between stocks
   - Respects free tier limits (5 calls/min, 25 calls/day)

## Customization 🎨

### Change Price Threshold
Edit the line with `if percentage_difference > 5:` in `main.py`:
```python
if percentage_difference > 5:  # Change 5 to your desired percentage
```

### Change Number of News Articles
Edit the line with `first_three_articles = articles[:3]` in `main.py`:
```python
first_three_articles = articles[:3]  # Change 3 to your desired count
```

### Add/Remove Stocks
Edit the `STOCKS` list at the top of `main.py`:
```python
STOCKS = [
    {"symbol": "YOUR_SYMBOL", "name": "Company Name"},
    # Add or remove as needed
]
```

### Change Email Format
Edit the `send_email()` function in `main.py` to customize the email template.

## Troubleshooting 🐛

| Issue | Solution |
|-------|----------|
| "API call limit exceeded" | Free tier has 25 calls/day. Reduce stock list or wait until next day. Upgrade Alpha Vantage plan. |
| "Email not sending" | Verify Gmail app password (not regular password). Check 2-Step Verification is enabled. |
| "No data for stock" | Symbol might be incorrect or market is closed. Alpha Vantage may be rate-limited. |
| "Task not running" | Check Python path is correct. Run Task Scheduler as Administrator. Check event logs. |
| ".env file not found" | Create `.env` in same folder as `main.py`. Check file is not named `.env.txt`. |

## API Limits 📊

| API | Free Tier | Premium |
|-----|-----------|---------|
| **Alpha Vantage** | 25 calls/day, 5/min | Paid plans available |
| **News API** | 100 requests/day | Paid plans available |
| **Gmail SMTP** | Unlimited (limited by Gmail) | Same |

**Tip**: With 15 stocks, you have ~1-2 runs per day before hitting Alpha Vantage limit.

## File Structure 📁

```
Day36-StockTradingNews/stock-news-normal-start/
├── main.py              # Main application script
├── .env                 # API keys (don't commit!)
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Security Best Practices 🔐

1. **Never commit `.env` to git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use App Passwords for Gmail**
   - Don't use your actual Gmail password
   - Generate app-specific password

3. **Rotate API Keys Periodically**
   - Regenerate Alpha Vantage key quarterly
   - Check News API dashboard regularly

4. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade requests python-dotenv
   ```

## Performance Notes ⚡

- **Run Time**: ~2.5 minutes for 15 stocks (includes rate limiting delays)
- **API Calls**: 1 call per stock per run (15 calls total)
- **Email Time**: Depends on Gmail, typically <30 seconds
- **CPU Usage**: Minimal (mostly waiting for API responses)

## Future Enhancements 💡

- [ ] Slack/Discord notifications instead of email
- [ ] Configurable thresholds per stock
- [ ] Database logging of price history
- [ ] Real-time WebSocket updates (premium APIs)
- [ ] Python package for easy installation
- [ ] Web dashboard for viewing alerts
- [ ] Mobile app notifications
- [ ] Custom trading rules (e.g., buy at threshold)

## License 📜

Open source - feel free to modify and use for personal projects.

## Questions? 🤔

Check:
1. Alpha Vantage docs: https://www.alphavantage.co/documentation/
2. News API docs: https://newsapi.org/docs
3. Gmail App Passwords: https://support.google.com/accounts/answer/185833

Happy trading! 🚀
