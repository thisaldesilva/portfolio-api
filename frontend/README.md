# Portfolio Management Angular App

A modern Angular application for managing customer portfolios and stock investments.

## Features

- **Customer Management**: Create, view, update, and delete customers
- **Portfolio Management**: Add and manage stocks for each customer
- **Portfolio Returns**: Calculate returns over date ranges
- **Stock Browser**: View and populate stock data from Polygon API
- **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Node.js 20.x or 22.x (or use the provided simple server)
- npm or yarn

## Quick Start

### Option 1: Simple HTTP Server (No Build Required)

```bash
# Install a simple HTTP server
npm install -g http-server

# Serve the app
cd portfolio-app
http-server ./src -p 4200 -o
```

### Option 2: With Angular CLI (Full Development)

```bash
# Install Angular CLI globally
npm install -g @angular/cli@17

# Install dependencies
npm install

# Serve the app
ng serve --open
```

## Project Structure

```
portfolio-app/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── customer-list/      # List all customers
│   │   │   ├── customer-detail/    # View/edit customer
│   │   │   ├── customer-form/      # Create/update customer
│   │   │   ├── portfolio-returns/  # Calculate returns
│   │   │   └── stock-browser/      # Browse and populate stocks
│   │   ├── models/
│   │   │   ├── customer.model.ts   # Customer interfaces
│   │   │   └── stock.model.ts      # Stock interfaces
│   │   ├── services/
│   │   │   └── api.service.ts      # REST API service
│   │   ├── app.component.ts        # Root component
│   │   └── app.routes.ts           # App routing
│   ├── index.html                  # Main HTML file
│   └── main.ts                     # App bootstrap
├── package.json
├── tsconfig.json
└── README.md
```

## API Configuration

The app connects to: `http://34.230.181.107:8000/api/v1`

To change the API URL, edit `src/app/services/api.service.ts`:

```typescript
private apiUrl = 'http://your-api-url:8000/api/v1';
```

## Available Routes

- `/` - Home (Customer List)
- `/customers` - Customer List
- `/customers/new` - Create New Customer
- `/customers/:id` - Customer Detail
- `/customers/:id/edit` - Edit Customer
- `/customers/:id/returns` - Portfolio Returns
- `/stocks` - Stock Browser

## Development

### Running Tests

```bash
npm test
```

### Building for Production

```bash
ng build --configuration production
```

The build artifacts will be stored in the `dist/` directory.

## Technologies Used

- **Angular 17**: Modern web framework with standalone components
- **RxJS 7**: Reactive programming library
- **TypeScript**: Type-safe JavaScript
- **HttpClient**: For REST API communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

ISC
