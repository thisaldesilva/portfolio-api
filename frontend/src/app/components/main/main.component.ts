import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Customer, CustomerCreate, StockInput } from '../../models/customer.model';
import { Stock, PortfolioReturns } from '../../models/stock.model';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  // Active section tracking
  activeSection: string = 'customers';

  // Customers data
  customers: Customer[] = [];
  customersLoading: boolean = false;
  customersError: string = '';

  // Create customer form
  customerName: string = '';
  customerAddress: string = '';
  stockTicker: string = '';
  stockQuantity: number | null = null;
  selectedStocks: StockInput[] = [];
  createMessage: string = '';
  createMessageType: 'success' | 'error' | '' = '';
  createLoading: boolean = false;

  // Stocks section
  populateTicker: string = '';
  stocksMessage: string = '';
  stocksMessageType: 'success' | 'error' | '' = '';
  stocksLoading: boolean = false;

  // Returns section
  returnsCustomerId: string = '';
  returnsStartDate: string = '';
  returnsEndDate: string = '';
  returnsMessage: string = '';
  returnsMessageType: 'success' | 'error' | '' = '';
  returnsLoading: boolean = false;
  portfolioReturns: PortfolioReturns | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.setDefaultDates();
    this.loadCustomers();
  }

  // Section navigation
  showSection(sectionName: string): void {
    this.activeSection = sectionName;
    if (sectionName === 'customers') {
      this.loadCustomers();
    }
  }

  // Set default dates (today and 2 weeks ago)
  private setDefaultDates(): void {
    const today = new Date();
    const twoWeeksAgo = new Date(today.getTime() - 14 * 24 * 60 * 60 * 1000);

    this.returnsEndDate = this.formatDate(today);
    this.returnsStartDate = this.formatDate(twoWeeksAgo);
  }

  private formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  // Customers operations
  loadCustomers(): void {
    this.customersLoading = true;
    this.customersError = '';

    this.apiService.getCustomers().subscribe({
      next: (customers) => {
        this.customers = customers;
        this.customersLoading = false;
      },
      error: (error) => {
        this.customersError = `Error loading customers: ${error.message}`;
        this.customersLoading = false;
      }
    });
  }

  viewCustomer(customerId: string): void {
    this.returnsCustomerId = customerId;
    this.showSection('returns');
  }

  // Stock management in create customer form
  addStock(): void {
    const ticker = this.stockTicker.toUpperCase().trim();
    const quantity = this.stockQuantity;

    if (!ticker || !quantity || quantity < 1) {
      alert('Please enter valid ticker and quantity');
      return;
    }

    this.selectedStocks.push({ ticker, quantity });
    this.stockTicker = '';
    this.stockQuantity = null;
  }

  removeStock(index: number): void {
    this.selectedStocks.splice(index, 1);
  }

  // Create customer
  createCustomer(): void {
    if (!this.customerName || !this.customerAddress) {
      this.createMessage = 'Please fill in all required fields';
      this.createMessageType = 'error';
      return;
    }

    this.createLoading = true;
    this.createMessage = 'Creating customer...';
    this.createMessageType = '';

    const customerData: CustomerCreate = {
      name: this.customerName,
      address: this.customerAddress,
      stocks: this.selectedStocks.length > 0 ? this.selectedStocks : undefined
    };

    this.apiService.createCustomer(customerData).subscribe({
      next: (customer) => {
        this.createMessage = `Customer created successfully! ID: ${customer.id}`;
        this.createMessageType = 'success';
        this.createLoading = false;

        // Reset form
        this.customerName = '';
        this.customerAddress = '';
        this.selectedStocks = [];
        this.stockTicker = '';
        this.stockQuantity = null;

        // Reload customers list
        this.loadCustomers();
      },
      error: (error) => {
        this.createMessage = `Error: ${error.message}`;
        this.createMessageType = 'error';
        this.createLoading = false;
      }
    });
  }

  // Stock population
  populateStock(): void {
    const ticker = this.populateTicker.toUpperCase().trim();

    if (!ticker) {
      this.stocksMessage = 'Please enter a ticker symbol';
      this.stocksMessageType = 'error';
      return;
    }

    this.stocksLoading = true;
    this.stocksMessage = 'Populating stock data...';
    this.stocksMessageType = '';

    this.apiService.populateStock(ticker).subscribe({
      next: (stock) => {
        this.stocksMessage = `Stock ${stock.ticker} populated successfully!`;
        this.stocksMessageType = 'success';
        this.stocksLoading = false;
        this.populateTicker = '';
      },
      error: (error) => {
        this.stocksMessage = `Error: ${error.message}`;
        this.stocksMessageType = 'error';
        this.stocksLoading = false;
      }
    });
  }

  populateFortune500(): void {
    this.stocksLoading = true;
    this.stocksMessage = 'Starting Fortune 500 population...';
    this.stocksMessageType = '';

    this.apiService.populateFortune500().subscribe({
      next: (result) => {
        this.stocksMessage = result.message;
        this.stocksMessageType = 'success';
        this.stocksLoading = false;
      },
      error: (error) => {
        this.stocksMessage = `Error: ${error.message}`;
        this.stocksMessageType = 'error';
        this.stocksLoading = false;
      }
    });
  }

  // Portfolio returns
  calculateReturns(): void {
    if (!this.returnsCustomerId || !this.returnsStartDate || !this.returnsEndDate) {
      this.returnsMessage = 'Please fill in all fields';
      this.returnsMessageType = 'error';
      return;
    }

    this.returnsLoading = true;
    this.returnsMessage = 'Calculating returns...';
    this.returnsMessageType = '';
    this.portfolioReturns = null;

    this.apiService.getPortfolioReturns(
      this.returnsCustomerId,
      this.returnsStartDate,
      this.returnsEndDate
    ).subscribe({
      next: (returns) => {
        this.portfolioReturns = returns;
        this.returnsMessage = '';
        this.returnsLoading = false;
      },
      error: (error) => {
        this.returnsMessage = `Error: ${error.message}`;
        this.returnsMessageType = 'error';
        this.returnsLoading = false;
      }
    });
  }

  // Helper methods for template
  isPositive(value: number): boolean {
    return value >= 0;
  }

  formatNumber(value: number, decimals: number = 2): string {
    return value.toFixed(decimals);
  }
}
