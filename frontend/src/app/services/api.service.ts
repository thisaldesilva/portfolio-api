import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Customer, CustomerCreate, CustomerUpdate } from '../models/customer.model';
import { Stock, PortfolioReturns } from '../models/stock.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = '/api/v1';

  constructor(private http: HttpClient) {}

  // Customer endpoints
  getCustomers(): Observable<Customer[]> {
    return this.http.get<Customer[]>(`${this.apiUrl}/customers/`);
  }

  getCustomer(id: string): Observable<Customer> {
    return this.http.get<Customer>(`${this.apiUrl}/customers/${id}`);
  }

  createCustomer(customer: CustomerCreate): Observable<Customer> {
    return this.http.post<Customer>(`${this.apiUrl}/customers/`, customer);
  }

  updateCustomer(id: string, customer: CustomerUpdate): Observable<Customer> {
    return this.http.put<Customer>(`${this.apiUrl}/customers/${id}`, customer);
  }

  deleteCustomer(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/customers/${id}`);
  }

  // Stock endpoints
  getStock(ticker: string): Observable<Stock> {
    return this.http.get<Stock>(`${this.apiUrl}/stocks/${ticker}`);
  }

  populateStock(ticker: string): Observable<Stock> {
    return this.http.post<Stock>(`${this.apiUrl}/stocks/populate/${ticker}`, {});
  }

  populateFortune500(): Observable<{message: string, status: string}> {
    return this.http.post<{message: string, status: string}>(`${this.apiUrl}/stocks/populate-fortune500`, {});
  }

  // Portfolio endpoints
  getPortfolioReturns(customerId: string, startDate: string, endDate: string): Observable<PortfolioReturns> {
    const params = new HttpParams()
      .set('start_date', startDate)
      .set('end_date', endDate);
    return this.http.get<PortfolioReturns>(`${this.apiUrl}/portfolio/${customerId}/returns`, { params });
  }
}
