# Operis SaaS Platform  

Operis is a scalable SaaS platform designed for businesses to manage operations efficiently. The platform supports functionalities like user management, business associations, financial tracking, and modularity for future enhancements.

## Features  

- **User and Role Management**  
  - Separate logins for business owners and staff members.  
  - Role-based access to business-specific data.  

- **Business Association**  
  - Business owners can manage their businesses and associate users with specific roles.  

- **Financial Tracking**  
  - Record and manage expenses and revenues.  
  - Track and report financial data over time.  

- **Modular and Scalable Architecture**  
  - Built with Flask, HTMX, and Tailwind CSS for a seamless and dynamic experience.  
  - PostgreSQL on Neon with SQLAlchemy ORM for database operations.  

## Key Technologies  

- **Backend**: Flask framework with SQLAlchemy ORM  
- **Frontend**: HTMX for dynamic interactions and Tailwind CSS for design  
- **Database**: PostgreSQL on Neon with Flask-Migrate for schema management  

## Setup  

1. **Clone the repository**:  
   ```bash  
   git clone <repository-url>  
   cd operis  
   ```  

2. **Create a virtual environment and install dependencies**:  
   ```bash  
   python3 -m venv .venv  
   source .venv/bin/activate  
   pip install -r requirements.txt  
   ```  

3. **Set up the database**:  
   - Configure your database connection string in the environment variables.  
   - Run migrations:  
     ```bash  
     flask db upgrade  
     ```  

4. **Run the application**:  
   ```bash  
   flask run  
   ```  

## Development Highlights  

- **Signup Workflow**:  
  - Validates data with user-friendly error messages.  
  - Associates businesses and users upon signup.  
  - Displays a success message before redirecting to the dashboard.  

- **Error Handling**:  
  - Graceful handling of duplicate business names and database errors.  
  - Detailed server-side logging for debugging.  

- **User Experience Enhancements**:  
  - Added loaders to buttons during form submissions for better feedback.  
  - HTMX-powered partial updates for smoother user interactions.  

## Folder Structure  

- `app/models`: Database models (User, Business, Finance, etc.)  
- `app/crud`: Business logic for database interactions.  
- `app/routes`: API routes for handling user requests.  
- `app/templates`: HTML templates structured modularly for easy customization.  

## Future Plans  

- Integrate advanced analytics for financial insights.  
- Add support for multi-business ownership and data visualization.  
- Extend the platform to support other business domains like logistics and inventory management.  

## License  

This project is open-source. Feel free to contribute or use it as a foundation for your own projects.  