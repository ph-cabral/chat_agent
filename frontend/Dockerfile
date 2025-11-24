FROM node:18-alpine

WORKDIR /app

# Instalar pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copiar archivos de dependencias
COPY package.json ./

# Instalar dependencias
RUN pnpm install

# Copiar el resto del código
COPY . .

EXPOSE 3000

CMD ["pnpm", "dev", "--host"]