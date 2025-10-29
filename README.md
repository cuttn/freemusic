# 🎵 Spotify-DL: Your Music, Your Way

A little wrapper around yt-dlp that integrates with the Spotify API, letting you manage your music library through a cute web interface. You can download all your playlists, songs, albums, recently played, top artists and more!!

## ✨ Features

- Sign in with your Spotify account using OAuth2
- Download your entire library, playlists, or specific albums
- Clean, simple web interface
- Powered by yt-dlp under the hood

## 🚀 Getting Started

### Option 1: Docker (Recommended)

The easiest way to get up and running:

```bash
docker compose up --build -d
```

Then just head to `http://localhost:8000` and you're good to go!

### Option 2: Local Setup

If you prefer running things locally:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment:
   ```python IMPORTANTSETUP.py
   ```
4. Fire it up:
   ```bash
   django-admin runserver
   ```

## 🔑 API Setup

You'll need to create your own Spotify API key. If you have a large music collection, the setup process is well worth the effort! This tool was created to help music lovers have more control over their personal libraries.

*(Website coming soon! Keep an eye on this space for updates.)*



## � Technical Deep Dive

### Architecture and Technical Challenges

#### Asynchronous Processing Architecture
- Implemented cutting-edge async/await patterns in Django using `asgiref.sync_to_async` for high-performance concurrent operations
- Developed custom `AsyncSpotify` wrapper class to handle parallel API requests efficiently
- Engineered concurrent download system with intelligent chunking to prevent system overload
- Leveraged `asyncio.gather()` for optimal parallel execution of multiple downloads

#### API Integration and Data Flow
- Seamlessly integrated Spotify Web API with OAuth2 authentication flow
- Implemented sophisticated paginated data fetching with cursor-based pagination
- Built enterprise-grade error handling for API rate limits and connection issues
- Architected efficient caching mechanisms for API responses

#### Performance Optimizations
- Engineered chunked processing for large playlist downloads with dynamic chunk sizing
- Implemented async generators for memory-efficient stream processing
- Designed robust cleanup mechanisms using context managers and `finally` blocks
- Created automatic resource management system for temporary files and ZIP archives

#### Database Architecture
- Designed scalable Django models with efficient querying patterns
- Implemented advanced indexing strategies for optimized search performance
- Created robust data integrity checks and constraints
- Utilized Django's ORM for type-safe database operations

#### Security Implementations
- Engineered secure OAuth token management with session-based storage
- Implemented comprehensive CSRF protection
- Developed thorough input sanitization for file paths and names
- Created secure file operation handlers with proper permission management

#### Media Processing Pipeline
- Integrated yt-dlp with custom async wrapper for reliable media downloading
- Engineered concurrent media processing with asyncio for optimal performance
- Implemented automatic metadata tagging system for downloaded files
- Developed efficient ZIP compression for bulk downloads

### Technical Stack Highlights

#### Backend Technologies
- Django (Async Views)
- Python AsyncIO
- Spotipy (Spotify API Client)
- yt-dlp Integration

#### Infrastructure
- Asynchronous Server Gateway Interface (ASGI)
- Session Management System
- Concurrent File System Operations
- Memory-Optimized Processing

#### External Services Integration
- Spotify Web API
- YouTube Data API (via yt-dlp)
- OAuth2 Authentication Flow

#### Development and Deployment
- Docker Containerization
- Development/Production Environment Management
- Automated Cleanup Procedures

### Notable Technical Achievements
- Successfully engineered a concurrent download system that efficiently manages system resources
- Implemented sophisticated memory management for handling large media files
- Developed a robust error recovery system with automatic retry mechanisms
- Created a scalable architecture capable of handling multiple concurrent users
- Engineered efficient cleanup procedures for temporary files and sessions

## �📝 Note

This is a tool for personal use. Please respect artists and support them by using official platforms whenever possible.

````
