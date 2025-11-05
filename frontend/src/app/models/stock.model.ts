export interface Stock {
  ticker: string;
  name: string;
  exchange: string | null;
  created_at: string;
  updated_at: string;
}

export interface PortfolioReturns {
  customer_id: string;
  start_date: string;
  end_date: string;
  total_return: number;
  return_percentage: number;
  holdings: Holding[];
}

export interface Holding {
  ticker: string;
  quantity: number;
  start_price: number;
  end_price: number;
  start_value: number;
  end_value: number;
  return: number;
  return_percentage: number;
}
