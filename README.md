# Malzahratech Machine Maintenance Management System

Malzahratech is a platform for assest management(machines, vehicles, equipments), maintenace report , maintenance schedule, inventory management, predictive maintenance, preventive maintenance, live data analysis and reports and work order management.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)
  - [Signup](#signup)
  - [Login](#login)
  - [Forget Password](#forget-password)
  - [Reset Password](#reset-password)
  - [Logout](#logout)
- [Machine](#machine)
  - [Display All Machines](#display-all-machines)
  - [Add New Machine](#add-new-machine)
  - [Display a Machine](#display-a-machine)
  - [Edit a Machine](#edit-a-machine)
  - [Delete a Machine](#delete-a-machine)
- [Machine Maintenance Report](#machine-maintenance-report)
  - [Display All Maintenance Reports](#display-all-maintenance-reports)
  - [Add New Maintenance Report](#add-new-maintenance-report)
  - [Edit a Maintenance Report](#edit-a-maintenance-report)
  - [Delete a Maintenance Report](#delete-a-maintenance-report)
- [Maintenance Notification](#maintenance-notification)
  - [Display All Maintenance Notifications](#display-all-maintenance-notifications)
  - [Add New Maintenance Notification](#add-new-maintenance-notification)
  - [Display Maintenance Notifications by Report Date](#display-maintenance-notifications-by-report-date)
  - [Edit a Maintenance Notification](#edit-a-maintenance-notification)
  - [Delete a Maintenance Notification](#delete-a-maintenance-notification)
  - [Send Maintenance Notification via Email](#send-maintenance-notification-via-email)
- [Maintenance Schedule](#maintenance-schedule)
  - [Display All Maintenance Schedules](#display-all-maintenance-schedules)
  - [Add New Maintenance Schedule](#add-new-maintenance-schedule)
  - [Display Maintenance Schedules by Schedule Date](#display-maintenance-schedules-by-schedule-date)
  - [Edit a Maintenance Schedule](#edit-a-maintenance-schedule)
  - [Delete a Maintenance Schedule](#delete-a-maintenance-schedule)
  - [Send Maintenance Schedule via Email](#send-maintenance-schedule-via-email)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Malzahratech is a platform for assest management(machines, vehicles, equipments), maintenace report , maintenance schedule, inventory management, predictive maintenance, preventive maintenance, live data analysis and reports and work order management.

## Installation

malzahra.tech


## Authentication

### Signup

- **Route:** `/auth/signup`
- **Methods:** GET, POST
- **Description:** This route allows users to sign up for an account.
- **Functionality:**
  - Renders the signup form using the `SignupForm` class.
  - Validates form input data and displays appropriate error messages.
  - Checks if the user is already registered and displays an error message if the email address already exists.
  - Creates a new user and adds them to the database.
  - Displays flash messages for success or error.
  - Redirects to the login page.

### Login

- **Route:** `/auth/login`
- **Methods:** GET, POST
- **Description:** This route allows users to log in to their account.
- **Functionality:**
  - Renders the login form using the `LoginForm` class.
  - Validates form input data and displays appropriate error messages.
  - Checks if the user exists and verifies the password.
  - Logs in the user using `login_user` and sets the remember me option.
  - Redirects to the machines page upon successful login.
  - Displays flash messages for success or error.

### Forget Password

- **Route:** `/auth/forget_password`
- **Methods:** GET, POST
- **Description:** This route allows users to reset their password if they forget it.
- **Functionality:**
  - Renders the forget password form using the `ForgetPassword` class.
  - Validates form input data and displays appropriate error messages.
  - Sends a password reset email to the user's email address if it exists in the database.
  - Generates a reset token and stores it in the user's record.
  - Composes and sends an email with the reset token.
  - Displays flash messages for success or error.
  - Redirects to the login page.

### Reset Password

- **Route:** `/auth/reset_password/<token>`
- **Methods:** GET, POST
- **Description:** This route allows users to reset their password using a reset token.
- **Functionality:**
  - Verifies the reset token and retrieves the user associated with the token.
  - Renders the reset password form using the `ResetPassword` class.
  - Validates form input data and displays appropriate error messages.
  - Updates the user's password with the new password.
  - Removes the reset token from the user's record.
  - Displays flash messages for success or error.
  - Redirects to the login page.

### Logout

- **Route:** `/auth/logout`
- **Methods:** GET
- **Description:** This route allows authenticated users to log out of their account.
- **Functionality:**
  - Logs out the user using `logout_user`.
  - Displays flash message for successful logout.
  - Redirects to the login page.

## Machine

### Display All Machines

- **Route:** `/machine/all`
- **Methods:** GET
- **Description:** This route displays all machines in the user's database.
- **Functionality:**
  - Retrieves all machines from the database.
  - Renders the machine list template with the retrieved machines.

### Add New Machine

- **Route:** `/machine/add`
- **Methods:** GET, POST
- **Description:** This route allows users to add a new machine to the user's database.
- **Functionality:**
  - Renders the add machine form using the `AddMachineForm` class.
  - Validates form input data and displays appropriate error messages.
  - Creates a new machine and adds it to the user's database.
  - Displays flash messages for success or error.
  - Redirects to the machine list page upon successful addition.

### Display a Machine

- **Route:** `/machine/<machine_id>`
- **Methods:** GET
- **Description:** This route displays information about a specific machine.
- **Functionality:**
  - Retrieves the machine with the given `machine_id` from the database.
  - Renders the machine details template with the retrieved machine.

### Edit a Machine

- **Route:** `/machine/edit/<machine_id>`
- **Methods:** GET, POST
- **Description:** This route allows users to edit an existing machine in the user's database.
- **Functionality:**
  - Retrieves the machine with the given `machine_id` from the database.
  - Renders the edit machine form using the `EditMachineForm` class.
  - Validates form input data and displays appropriate error messages.
  - Updates the machine's details in the user's database.
  - Displays flash messages for success or error.
  - Redirects to the machine details page upon successful edit.

### Delete a Machine

- **Route:** `/machine/delete/<machine_id>`
- **Methods:** GET
- **Description:** This route allows users to delete a machine from the user's database.
- **Functionality:**
  - Retrieves the machine with the given `machine_id` from the database.
  - Deletes the machine from the user's database.
  - Displays flash message for successful deletion.
  - Redirects to the machine list page.

## Machine Maintenance Report

### Display All Maintenance Reports

- **Route:** `/machine/maintenance-reports/all`
- **Methods:** GET
- **Description:** This route displays all machine maintenance reports based on the machine's serial number.
- **Functionality:**
  - Retrieves all maintenance reports associated with the machine's serial number.
  - Renders the maintenance report list template with the retrieved reports.

### Add New Maintenance Report

- **Route:** `/machine/maintenance-report/add/<machine_serial_number>`
- **Methods:** GET, POST
- **Description:** This route allows users to add a new maintenance report for a machine.
- **Functionality:**
  - Retrieves the machine with the given `machine_serial_number` from the database.
  - Renders the add maintenance report form using the `AddMaintenanceReportForm` class.
  - Validates form input data and displays appropriate error messages.
  - Creates a new maintenance report for the machine.
  - Displays flash messages for success or error.
  - Redirects to the maintenance report list page upon successful addition.

### Edit a Maintenance Report

- **Route:** `/machine/maintenance-report/edit/<report_id>`
- **Methods:** GET, POST
- **Description:** This route allows users to edit a maintenance report.
- **Functionality:**
  - Retrieves the maintenance report with the given `report_id` from the database.
  - Renders the edit maintenance report form using the `EditMaintenanceReportForm` class.
  - Validates form input data and displays appropriate error messages.
  - Updates the maintenance report's details.
  - Displays flash messages for success or error.
  - Redirects to the maintenance report list page upon successful edit.

### Delete a Maintenance Report

- **Route:** `/machine/maintenance-report/delete/<report_id>`
- **Methods:** GET
- **Description:** This route allows users to delete a maintenance report.
- **Functionality:**
  - Retrieves the maintenance report with the given `report_id` from the database.
  - Deletes the maintenance report.
  - Displays flash message for successful deletion.
  - Redirects to the maintenance report list page.

## Maintenance Notification

### Display All Maintenance Notifications

- **Route:** `/maintenance-notifications/all`
- **Methods:** GET
- **Description:** This route displays all maintenance notifications.
- **Functionality:**
  - Retrieves all maintenance notifications from the database.
  - Renders the maintenance notification list template with the retrieved notifications.

### Add New Maintenance Notification

- **Route:** `/maintenance-notification/add/<machine_serial_number>`
- **Methods:** GET, POST
- **Description:** This route allows users to add a new maintenance notification for a machine.
- **Functionality:**
  - Retrieves the machine with the given `machine_serial_number` from the database.
  - Renders the add maintenance notification form using the `AddMaintenanceNotificationForm` class.
  - Validates form input data and displays appropriate error messages.
  - Creates a new maintenance notification for the machine.
  - Displays flash messages for success or error.
  - Redirects to the maintenance notification list page upon successful addition.

### Display Maintenance Notifications by Report Date

- **Route:** `/maintenance-notifications/report-date/<machine_serial_number>`
- **Methods:** GET
- **Description:** This route displays maintenance notifications based on the report date.
- **Functionality:**
  - Retrieves the machine with the given `machine_serial_number` from the database.
  - Retrieves maintenance notifications associated with the machine, sorted by the report date.
  - Renders the maintenance notification list template with the retrieved notifications.

### Edit a Maintenance Notification

- **Route:** `/maintenance-notification/edit/<notification_id>`
- **Methods:** GET, POST
- **Description:** This route allows users to edit a maintenance notification.
- **Functionality:**
  - Retrieves the maintenance notification with the given `notification_id` from the database.
  - Renders the edit maintenance notification form using the `EditMaintenanceNotificationForm` class.
  - Validates form input data and displays appropriate error messages.
  - Updates the maintenance notification's details.
  - Displays flash messages for success or error.
  - Redirects to the maintenance notification list page upon successful edit.

### Delete a Maintenance Notification

- **Route:** `/maintenance-notification/delete/<notification_id>`
- **Methods:** GET
- **Description:** This route allows users to delete a maintenance notification.
- **Functionality:**
  - Retrieves the maintenance notification with the given `notification_id` from the database.
  - Deletes the maintenance notification.
  - Displays flash message for successful deletion.
  - Redirects to the maintenance notification list page.

### Send Maintenance Notification via Email

- **Route:** `/maintenance-notification/send-email/<notification_id>`
- **Methods:** GET
- **Description:** This route allows users to send a maintenance notification via email.
- **Functionality:**
  - Retrieves the maintenance notification with the given `notification_id` from the database.
  - Sends an email to the specified recipients with the maintenance notification details.
  - Displays flash message for successful email sending.
  - Redirects to the maintenance notification list page.

## Maintenance Schedule

### Display All Maintenance Schedules

- **Route:** `/maintenance-schedules/all`
- **Methods:** GET
- **Description:** This route displays all maintenance schedules.
- **Functionality:**
  - Retrieves all maintenance schedules from the database.
  - Renders the maintenance schedule list template with the retrieved schedules.

### Add New Maintenance Schedule

- **Route:** `/maintenance-schedule/add/<machine_serial_number>`
- **Methods:** GET, POST
- **Description:** This route allows users to add a new maintenance schedule for a machine.
- **Functionality:**
  - Retrieves the machine with the given `machine_serial_number` from the database.
  - Renders the add maintenance schedule form using the `AddMaintenanceScheduleForm` class.
  - Validates form input data and displays appropriate error messages.
  - Creates a new maintenance schedule for the machine.
  - Displays flash messages for success or error.
  - Redirects to the maintenance schedule list page upon successful addition.

### Display Maintenance Schedules by Schedule Date

- **Route:** `/maintenance-schedules/schedule-date/<machine_serial_number>`
- **Methods:** GET
- **Description:** This route displays maintenance schedules based on the schedule date.
- **Functionality:**
  - Retrieves the machine with the given `machine_serial_number` from the database.
  - Retrieves maintenance schedules associated with the machine, sorted by the schedule date.
  - Renders the maintenance schedule list template with the retrieved schedules.

### Edit a Maintenance Schedule

- **Route:** `/maintenance-schedule/edit/<schedule_id>`
- **Methods:** GET, POST
- **Description:** This route allows users to edit a maintenance schedule.
- **Functionality:**
  - Retrieves the maintenance schedule with the given `schedule_id` from the database.
  - Renders the edit maintenance schedule form using the `EditMaintenanceScheduleForm` class.
  - Validates form input data and displays appropriate error messages.
  - Updates the maintenance schedule's details.
  - Displays flash messages for success or error.
  - Redirects to the maintenance schedule list page upon successful edit.

### Delete a Maintenance Schedule

- **Route:** `/maintenance-schedule/delete/<schedule_id>`
- **Methods:** GET
- **Description:** This route allows users to delete a maintenance schedule.
- **Functionality:**
  - Retrieves the maintenance schedule with the given `schedule_id` from the database.
  - Deletes the maintenance schedule.
  - Displays flash message for successful deletion.
  - Redirects to the maintenance schedule list page.

### Send Maintenance Schedule via Email

- **Route:** `/maintenance-schedule/send-email/<schedule_id>`
- **Methods:** GET
- **Description:** This route allows users to send a maintenance schedule via email.
- **Functionality:**
  - Retrieves the maintenance schedule with the given `schedule_id` from the database.
  - Sends an email to the specified recipients with the maintenance schedule details.
  - Displays flash message for successful email sending.
  - Redirects to the maintenance schedule list page.

## Technology Stack

- Python
- Flask
- Flask-WTF
- Flask-Mail
- Flask-Login
- SQLAlchemy
- MySQL

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
