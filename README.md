<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>UpvoteBot</h1>
    <p><strong>UpvoteBot</strong> is a simple bot that automatically upvotes posts on the "communities.win" website using Selenium WebDriver with Python. The bot navigates through posts, upvotes them if they are not already upvoted, and simulates human-like interactions (scrolling and random delays) to avoid detection.</p>
    <h2>Features</h2>
    <ul>
        <li><strong>Login Automation:</strong> Automatically logs into the target website using provided credentials.</li>
        <li><strong>Upvoting Posts:</strong> Identifies posts that haven't been upvoted yet and clicks the upvote button.</li>
        <li><strong>Human-like Interaction:</strong> Simulates human scrolling and clicks with randomized delays between actions.</li>
        <li><strong>Error Logging:</strong> Logs any errors or exceptions to a log file (<code>likebot-error.log</code>).</li>
        <li><strong>Custom Headers:</strong> Custom headers are applied to avoid detection.</li>
    </ul>
    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>Chrome Browser</li>
        <li>ChromeDriver (managed by <code>webdriver-manager</code>)</li>
        <li>Selenium WebDriver</li>
        <li><code>webdriver-manager</code> Python package</li>
        <li><code>time</code>, <code>random</code>, <code>logging</code> modules (standard Python libraries)</li>
    </ul>
    <h2>Installation</h2>
    <ol>
        <li><strong>Clone this repository</strong>:
            <pre><code>git clone https://github.com/Riotcoke123/upvotebot.git
cd upvotebot</code></pre>
        </li>
        <li><strong>Install the required dependencies</strong>:
            <pre><code>pip install -r requirements.txt</code></pre>
            If <code>requirements.txt</code> doesn't exist, run the following commands to install the necessary libraries:
            <pre><code>pip install selenium
pip install webdriver-manager</code></pre>
        </li>
    </ol>
    <h2>Usage</h2>
    <ol>
        <li>Replace <code>USERNAME</code> and <code>PASSWORD</code> with your login credentials.</li>
        <li>Run the script:
            <pre><code>python upvotebot.py</code></pre>
            This will start the bot, log you in, and begin upvoting posts automatically.
        </li>
        <li>The bot will continue to scroll and upvote posts in a loop. To stop the bot, press <code>CTRL + C</code>.</li>
    </ol>
    <h2>API Keys for IP2</h2>
    <p>To use the API for IP2 (like the <code>x-api-key</code>, <code>x-api-secret</code>, and <code>x-xsrf-token</code>), you can refer to the official <a href="https://docs.scored.co/" target="_blank">Scored API Documentation</a>. The API requires authentication and allows you to make requests to the endpoint <code>https://api.scored.co/api/v2/</code>.</p>
    <p>Follow the provided guidelines to generate your keys and tokens. Keep in mind the rate limits and terms of use that must be adhered to while interacting with the API.</p>
    <h2>Known Issues</h2>
    <p><strong>Bug:</strong> The bot skips some posts for upvoting, even though they haven't been upvoted yet. This may occur due to the logic used to track already upvoted posts, or due to a delay in page rendering that causes the upvote button to be temporarily unavailable. This issue is under investigation and may require further debugging.</p>
    <h2>License</h2>
    <p>This project is licensed under the <a href="https://www.gnu.org/licenses/agpl-3.0.html">GNU General Public License v3.0</a> - see the <a href="LICENSE">LICENSE</a> file for details.</p>
    <h2>Contributing</h2>
    <p>Feel free to fork this repository, create issues, and submit pull requests for bug fixes or improvements.</p>
    <h2>Troubleshooting</h2>
    <p>If you encounter any issues, please check the <code>likebot-error.log</code> file for error messages. You can also open an issue on the <a href="https://github.com/Riotcoke123/upvotebot/issues">GitHub Issues</a> page.</p>
    <h2>Disclaimer</h2>
    <p>This bot is for educational purposes only. Use it responsibly and be aware of the potential ethical and legal implications of automating interactions on websites.</p>
</body>
</html>
