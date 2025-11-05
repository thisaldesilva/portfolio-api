export interface Customer {
  id: string;
  name: string;
  address: string;
  created_at: string;
  updated_at: string;
  portfolio_stocks: PortfolioStock[];
}

export interface PortfolioStock {
  stock_ticker: string;
  quantity: number;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreate {
  name: string;
  address: string;
  stocks?: StockInput[];
}

export interface CustomerUpdate {
  name?: string;
  address?: string;
  stocks?: StockInput[];
}

export interface StockInput {
  ticker: string;
  quantity: number;
}
