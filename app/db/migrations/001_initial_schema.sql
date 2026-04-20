-- Initial schema for ZAD
-- Run via Supabase dashboard or CLI: supabase db push

-- User profiles (extends Supabase auth.users)
create table if not exists public.profiles (
    id          uuid primary key references auth.users(id) on delete cascade,
    email       text not null unique,
    full_name   text not null,
    phone       text,
    role        text not null default 'customer' check (role in ('customer', 'admin', 'vendor')),
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);

-- Products
create table if not exists public.products (
    id              uuid primary key default gen_random_uuid(),
    name            text not null,
    description     text,
    price           numeric(10, 2) not null check (price >= 0),
    category        text not null,
    stock_quantity  int not null default 0 check (stock_quantity >= 0),
    image_url       text,
    is_available    boolean not null default true,
    vendor_id       uuid references public.profiles(id) on delete set null,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

-- Cart items (no separate cart table; items are per-user)
create table if not exists public.cart_items (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null references public.profiles(id) on delete cascade,
    product_id  uuid not null references public.products(id) on delete cascade,
    quantity    int not null check (quantity > 0),
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now(),
    unique (user_id, product_id)
);

-- Orders
create table if not exists public.orders (
    id                  uuid primary key default gen_random_uuid(),
    user_id             uuid not null references public.profiles(id) on delete restrict,
    status              text not null default 'pending'
                            check (status in ('pending','confirmed','processing','shipped','delivered','cancelled')),
    total_amount        numeric(12, 2) not null check (total_amount >= 0),
    shipping_address    jsonb not null,
    notes               text,
    created_at          timestamptz not null default now(),
    updated_at          timestamptz not null default now()
);

-- Order items (snapshot of product at purchase time)
create table if not exists public.order_items (
    id              uuid primary key default gen_random_uuid(),
    order_id        uuid not null references public.orders(id) on delete cascade,
    product_id      uuid references public.products(id) on delete set null,
    product_name    text not null,
    unit_price      numeric(10, 2) not null check (unit_price >= 0),
    quantity        int not null check (quantity > 0),
    created_at      timestamptz not null default now()
);

-- Indexes
create index if not exists idx_products_category on public.products(category);
create index if not exists idx_products_available on public.products(is_available);
create index if not exists idx_cart_items_user on public.cart_items(user_id);
create index if not exists idx_orders_user on public.orders(user_id);
create index if not exists idx_orders_status on public.orders(status);
create index if not exists idx_order_items_order on public.order_items(order_id);
