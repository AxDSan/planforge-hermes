# PlanForge Mini App — Telegram WebApp

A lightweight Telegram Mini App for PlanForge project management. Runs inside Telegram as a native-feeling interface.

## What it does

- View current project status and phase progress
- See task lists with check/uncheck
- Read and update `.planning/` files
- Trigger Hermes commands via bot API

## Architecture

```
telegram-miniapp/
├── index.html          # Entry point (Telegram WebApp init)
├── app.js              # Main logic
├── styles.css          # Telegram-native styling
└── api.js              # Bridge to Hermes backend
```

## Telegram Bot Setup

1. Create bot with @BotFather
2. Enable WebApp: `/setinline` + `/setwebapp`
3. Set WebApp URL to your hosted mini app
4. User clicks button → WebApp opens inside Telegram

## How it connects to PlanForge

The Mini App reads `.planning/` files from the project directory. Since it runs in the browser, it needs a small API bridge (can be a local HTTP server or Hermes webhook) to read/write files.

## Deployment

Host as static files on Vercel, GitHub Pages, or any CDN. The WebApp URL must be HTTPS.
