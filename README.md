# Domain Monitor

### Planned Features
- DNS monitoring: A, AAAA, MX, and TXT records
  - Scanning engine (cron)
  - SSL details
- WHOIS Data Monitoring: 
  - Registrar details
  - Registration and expiration dates
  - Name servers
  - Registrant information (if available)
- Alert System
  - Email, SMS, webhooks
- UI
  - add domain
  - dns / whois changes
  - update alerts
- Message Queue for distributing monitoring tasks rabbit mq
  - async processing: do not block sender
  - decouple services
  - can easily add more consumers
  - reliable message delivery (persistent queues even if a service fails)
  - load balacning: distribute traffic across multiple consumers
- Caching (redis) 
- Rate limiting
- input validation / sanitation
