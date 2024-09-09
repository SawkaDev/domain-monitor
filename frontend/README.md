# DNS Monitoring Service Frontend

This is the frontend application for the DNS Monitoring Service, built with Next.js. It provides a user-friendly interface for users to search, view, and monitor domain information in real-time.

## Features

- **Domain Search**: Quickly search for any domain to view its DNS information.
- **Comprehensive Domain Profile**: View detailed information about a domain, including:
  - WHOIS data
  - Current DNS records
  - DNS history
  - WHOIS history
- **Real-time Monitoring**: Set up email/sms (mocked for now) notifications for changes to specific domains.
- **Pagination**: Efficiently browse through large sets of domain data with our paginated interface.

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm or yarn

### Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   git clone https://github.com/SawkaDev/domain-monitor.git

2. Navigate to the project directory:
   cd frontend

3. Install dependencies:
   - Using npm:
     npm install
   - Or, if you're using Yarn:
     yarn install

4. Start the development server:
   - Using npm:
     npm run dev
   - Or, using Yarn:
     yarn dev

6. Open [http://localhost:3010](http://localhost:3010) in your browser to see the application.

## Usage

- **Search for a Domain**: Use the search bar on the homepage to look up any domain (for new domains we will setup monitoring. From there on out we will track DNS/WHOIS changes).
- **Subscribe to Notifications**: On a domain's profile page, click the "Get Notifications" button to set up alerts for changes.
- **Navigate Through Data**: On each domain's profile page you can view an overivew, DNS history, and WHOIS history.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape this project.
- Special thanks to the Next.js and React Query communities for their excellent tools and documentation.
