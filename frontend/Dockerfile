FROM node:20-alpine AS base
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    NEXT_DISABLE_TURBOPACK=1

FROM base AS deps
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && pnpm install --frozen-lockfile

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN corepack enable \
 && pnpm build \
 && pnpm prune --prod

FROM base AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY package.json pnpm-lock.yaml* ./
EXPOSE 3000
CMD ["node", "./node_modules/next/dist/bin/next", "start", "-p", "3000"]
