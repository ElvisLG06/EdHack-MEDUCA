# Overview

MEDUCA (Sistema de Evaluación Matemática Inteligente) is an educational web platform designed for mathematics teachers in primary (grades 1-6) and secondary (grades 1-5) education. The system enables intelligent exam generation based on mathematical competencies, student management, and automated grading with AI-powered feedback. The platform follows a hierarchical structure: Course → Class → Competency → Exam, where teachers create courses, assign students to classes linked to specific mathematical competencies, and generate both pre-tests and post-tests using AI assistance.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5.3 dark theme for responsive UI
- **Client-Side**: Vanilla JavaScript with Feather Icons for iconography
- **Styling**: Custom CSS with CSS variables for consistent theming across the platform
- **Layout**: Hierarchical navigation with breadcrumbs and role-based dashboards

## Backend Architecture
- **Web Framework**: Flask with Werkzeug middleware for proxy handling
- **Authentication**: Session-based authentication with password hashing using Werkzeug security
- **Data Management**: In-memory data store using Python dictionaries for MVP implementation
- **File Handling**: Secure file upload system for exam images with 16MB size limit
- **PDF Generation**: ReportLab library for creating printable exam documents

## Data Storage Solutions
- **Current**: In-memory Python dictionaries organized by entity type (users, courses, classes, exams)
- **Models**: Simple Python classes representing User, Course, Class, Exam, and ExamenResuelto entities
- **File Storage**: Local filesystem storage for uploaded exam images in static/uploads directory
- **Session Management**: Flask sessions with configurable secret key for user authentication

## Authentication and Authorization
- **Role-Based Access**: Two user roles (docente/teacher and estudiante/student) with different permissions
- **Login System**: Username/password authentication with password hashing
- **Authorization Decorators**: Custom decorators (@login_required, @docente_required) for route protection
- **Session Security**: Configurable session secret key with environment variable fallback

# External Dependencies

## AI Services
- **Google Gemini API**: Used through google.genai client for generating evaluation criteria and exam feedback
- **Model**: Gemini-2.5-flash for text generation tasks
- **API Key**: Configurable via GEMINI_API_KEY or GOOGLE_API_KEY environment variables

## Core Python Libraries
- **Flask**: Web framework for routing and request handling
- **Werkzeug**: WSGI utilities and security functions for password hashing
- **ReportLab**: PDF generation library for creating printable exams
- **Logging**: Built-in Python logging for debugging and monitoring

## Frontend Dependencies
- **Bootstrap 5.3**: CSS framework with Replit's dark theme variant
- **Feather Icons**: Icon library loaded via CDN
- **CDN Dependencies**: All frontend libraries served from external CDNs

## Mathematical Competencies
- **Predefined Standards**: Hardcoded mathematical competencies for each grade level (1-11)
- **Curriculum Alignment**: Based on educational standards for primary and secondary mathematics
- **Competency Categories**: Four main areas - quantity, patterns/equivalence/change, data management/uncertainty, and form/movement/location