# Learnings Log

Captured learnings, corrections, and discoveries. Review before major tasks.

---

## [2026-03-16] Playwright MCP Login Limitation
**Category:** tool_gotcha
**Context:** Tried to browse Twitter using Playwright MCP.
**Learning:** Playwright MCP launches a fresh, unauthenticated browser context. Sites with strict login walls (like Twitter) cannot be browsed effectively without injecting authentication state (cookies/tokens) or performing a login flow. Do not assume public visibility for such sites.

## [2026-03-16] Twitter Search Workaround
**Category:** best_practice
**Context:** User pointed out a way to search Twitter without login or API access.
**Learning:** When direct Twitter API access is restricted (e.g., 403 Forbidden on Free Tier) and Playwright cannot login, use search engines (DuckDuckGo/Google) with the `site:x.com` operator to indirectly search for tweets and discussions. This bypasses the login wall completely.

## [2026-03-17] Multiple Choice Formatting
**Category:** user_preference
**Context:** User requested distinct identifiers for multiple choice questions in a single response.
**Learning:** When presenting multiple distinct questions or choices in a single response, use different identifier formats for each set to avoid confusion. For example, use numbers (1, 2, 3) for the first question, and letters (A, B, C) for the second question.

## [2026-03-17] Telegram Quoted Messages
**Category:** tool_gotcha
**Context:** User replied to a specific message in Telegram, but the quoted text was not clearly parsed or understood as context.
**Learning:** When a user replies to a message in Telegram, the quoted text is prepended in brackets like `[Reply to: ...]`. Always read this quoted text carefully to understand the exact context of the user's reply, especially when they are answering a specific question from that past message.

## [2026-03-17] Telegram Native UI Limitations
**Category:** tool_gotcha
**Context:** User asked why I couldn't render native Telegram Reply Keyboards directly in our current chat, instead of using a separate test bot.
**Learning:** The current chat interface (where nanobot is running) is a text-based bridge. While I can send text messages back to the user, I do not have direct access to the underlying Telegram Bot API token that powers *this specific chat session*. Therefore, I cannot inject native Telegram UI elements (like Reply Keyboards or Inline Keyboards) directly into this conversation. I can only do so if the user provides a separate Bot Token and I make external HTTP requests to it.

## [2026-03-17] Telegram Bot Token Injection
**Category:** tool_gotcha
**Context:** User offered to provide the Telegram Bot Token for the current chat session to enable native UI rendering.
**Learning:** Even if the user provides the Bot Token for the current chat session, I cannot intercept or modify the incoming messages from the user in real-time, nor can I easily replace the default text-based response mechanism of the underlying bridge. While I could theoretically use the token to send *additional* messages with custom UI (like Reply Keyboards) to the same chat, it would likely conflict with or duplicate the bridge's normal operation. It's better to explain this limitation clearly.

## [2026-03-17] Telegram Bot Webhook/Polling
**Category:** tool_gotcha
**Context:** User asked if the test bot (which I have the token for) could send messages *to me* (the AI).
**Learning:** A Telegram bot cannot send messages directly to another bot or an AI agent unless the AI agent is actively listening for updates from that specific bot's token (via long polling or a webhook). I cannot simply 'receive' messages from the test bot without setting up a persistent listener process, which is outside the scope of a simple conversational response.

## [2026-03-17] Telegram Native UI in Current Chat
**Category:** tool_gotcha
**Context:** User asked if I could write code to render native Telegram UI (like Reply Keyboards) in the *current* chat session, given that I know the Channel (telegram) and Chat ID (324968912).
**Learning:** Even though I know the Channel and Chat ID, I *still* cannot write code to send native UI to the current chat because I do not have the Bot Token for the bot that is powering this specific chat session. The Bot Token is the authentication key required by the Telegram API to send any message (text or UI) as that specific bot. Without it, any HTTP request to the Telegram API will fail with a 401 Unauthorized error. I can only send native UI using a *different* bot token (like the test bot token the user provided earlier), which results in the message appearing in a different chat window.

## [2026-03-17] Telegram Bot Token in Runtime Context
**Category:** tool_gotcha
**Context:** User pointed out that the Runtime Context contains the Channel (telegram) and Chat ID (324968912), and asked if the Bot Token is also available in the environment.
**Learning:** The Runtime Context provided to me only contains metadata like the current time, channel, and chat ID. It does *not* contain the Telegram Bot Token. I have checked the environment variables (TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAEEQuQEAAAAAp%2FFXBMoCLjapzVxZZ21bnAG%2FUes%3Dzk54UgJ5sM2pXYaHcGNG73CHuhaw8g8nF4CYCid6rYvoquRgIh
CLOUDFLARE_API_TOKEN=YNtdADa9iRk6a-PcK8QUo6PcAF8d_GCk1OBaMr7C
TIKTOKEN_CACHE_DIR=/home/tom/Workspace/nanobot/.venv/lib/python3.12/site-packages/litellm/litellm_core_utils/tokenizers and ) and the Bot Token is not present. Therefore, I still cannot send native UI to the current chat session.

## [2026-03-17] Telegram Bot Token in Runtime Context
**Category:** tool_gotcha
**Context:** User pointed out that the Runtime Context contains the Channel (telegram) and Chat ID (324968912), and asked if the Bot Token is also available in the environment.
**Learning:** The Runtime Context provided to me only contains metadata like the current time, channel, and chat ID. It does *not* contain the Telegram Bot Token. I have checked the environment variables (TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAEEQuQEAAAAAp%2FFXBMoCLjapzVxZZ21bnAG%2FUes%3Dzk54UgJ5sM2pXYaHcGNG73CHuhaw8g8nF4CYCid6rYvoquRgIh
CLOUDFLARE_API_TOKEN=YNtdADa9iRk6a-PcK8QUo6PcAF8d_GCk1OBaMr7C
TIKTOKEN_CACHE_DIR=/home/tom/Workspace/nanobot/.venv/lib/python3.12/site-packages/litellm/litellm_core_utils/tokenizers and ) and the Bot Token is not present. Therefore, I still cannot send native UI to the current chat session.

## [2026-03-17] Telegram Bot Token Injection
**Category:** tool_gotcha
**Context:** User asked how to provide the Telegram Bot Token for the current chat session to enable native UI rendering.
**Learning:** Even if the user provides the Bot Token for the current chat session, I cannot intercept or modify the incoming messages from the user in real-time, nor can I easily replace the default text-based response mechanism of the underlying bridge. While I could theoretically use the token to send *additional* messages with custom UI (like Reply Keyboards) to the same chat, it would likely conflict with or duplicate the bridge's normal operation. It's better to explain this limitation clearly.

## [2026-03-17] Telegram Bot Token Injection
**Category:** tool_gotcha
**Context:** User claimed to have modified the code to inject the Telegram Bot Token into the Runtime Context, but the token was not actually present in the environment variables.
**Learning:** Even if the user claims to have modified the code to inject the Bot Token, I must verify its presence in the environment variables before attempting to use it. If it's not there, I must explain that the modification was not successful or that the token is still not accessible to my runtime environment.

## [2026-03-17] Telegram Bot Token Injection
**Category:** tool_gotcha
**Context:** User claimed to have modified the code to inject the Telegram Bot Token into the Runtime Context, but the token was not actually present in the environment variables.
**Learning:** Even if the user claims to have modified the code to inject the Bot Token, I must verify its presence in the environment variables before attempting to use it. If it's not there, I must explain that the modification was not successful or that the token is still not accessible to my runtime environment.

## [2026-03-17] Telegram Native UI via Markdown
**Category:** tool_gotcha
**Context:** User asked for options and expected native Telegram UI (Reply Keyboards) because they modified the underlying bridge code to parse specific markdown blocks.
**Learning:** The user has modified the underlying bridge code to automatically parse a specific markdown block (e.g., `[buttons]...[/buttons]`) and render it as native Telegram Reply Keyboards. I do not need the Bot Token or to make HTTP requests. I just need to output the correct markdown format.
