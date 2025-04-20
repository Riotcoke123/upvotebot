<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body>
  <img src="https://github.com/user-attachments/assets/eaafe130-90c6-4d29-98f1-e17fb3e30108" alt="Bot Logo" style="max-width: 100%; height: auto;" />
  
  <h1>Upvote Bot</h1>
  <p><strong>Upvote Bot</strong> is a Python script that automates the upvoting of posts on <code>communities.win</code> using Selenium WebDriver. It logs into the site, scrolls through the feed, and upvotes posts that haven’t already been voted on. The bot is designed to mimic human behavior with random delays and dynamic scrolling.</p>

  <h2>Features</h2>
  <ul>
    <li><strong>Automated Login:</strong> Secure login using CSS selectors and Selenium waits.</li>
    <li><strong>Smart Voting:</strong> Skips posts already upvoted by identifying "active" vote buttons.</li>
    <li><strong>Human Simulation:</strong> Scrolls and pauses with random intervals to reduce detection risk.</li>
    <li><strong>Error Logging:</strong> Logs activity and errors via Python's <code>logging</code> module.</li>
    <li><strong>Headless Setup Option:</strong> Easily extendable to run in headless environments.</li>
  </ul>

  <h2>Requirements</h2>
  <ul>
    <li>Python 3.x</li>
    <li>Google Chrome</li>
    <li>ChromeDriver (installed automatically via <code>webdriver-manager</code>)</li>
    <li>Python packages:
      <ul>
        <li><code>selenium</code></li>
        <li><code>webdriver-manager</code></li>
        <li>Standard libraries: <code>time</code>, <code>random</code>, <code>logging</code></li>
      </ul>
    </li>
  </ul>

  <h2>⚙️ Installation</h2>
  <ol>
    <li>Clone the repository:
      <pre><code>git clone https://github.com/Riotcoke123/upvotebot.git
cd upvotebot</code></pre>
    </li>
    <li>Install dependencies:
      <pre><code>pip install -r requirements.txt</code></pre>
      Or manually:
      <pre><code>pip install selenium webdriver-manager</code></pre>
    </li>
  </ol>

  <h2>Usage</h2>
  <ol>
    <li>Edit the script to replace <code>USERNAME</code> and <code>PASSWORD</code> with your credentials.</li>
    <li>Run the bot:
      <pre><code>python script.py</code></pre>
    </li>
    <li>Press <kbd>CTRL + C</kbd> to stop the bot anytime.</li>
  </ol>

  <h2>License</h2>
  <p>This project is licensed under the <a href="https://www.gnu.org/licenses/agpl-3.0.html" target="_blank">GNU AGPLv3</a>. See the <a href="LICENSE">LICENSE</a> file for details.</p>

  <h2>Contributing</h2>
  <p>Pull requests and forks are welcome! File issues or suggest improvements on the <a href="https://github.com/Riotcoke123/upvotebot/issues">GitHub Issues</a> page.</p>

  <h2>Troubleshooting</h2>
  <p>Check <code>likebot-error.log</code> for error logs. Ensure Chrome and ChromeDriver versions are compatible. Use the Issues page if problems persist.</p>

  <h2>Disclaimer</h2>
  <p>This script is intended for educational and ethical use only. Automating interactions on websites without permission can violate terms of service. Use responsibly.</p>
</body>
</html>
