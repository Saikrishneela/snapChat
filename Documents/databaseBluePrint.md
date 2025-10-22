erDiagram
    %% =========================
    %% ENTITY DEFINITIONS
    %% =========================

    
    USER {
        int id PK
        string username
        string email
        string password
        datetime date_joined
    }

    SNAP {
        int id PK
        int sender_id FK
        string media_url
        datetime sent_at
        int duration_seconds
    }

    SNAP_VIEW {
        int id PK
        int snap_id FK
        int viewer_id FK
        datetime viewed_at
    }

    STORY {
        int id PK
        int creator_id FK
        string media_url
        datetime created_at
        datetime expires_at
    }

    STORY_VIEW {
        int id PK
        int story_id FK
        int viewer_id FK
        datetime viewed_at
    }

    FRIEND_REQUEST {
        int id PK
        int sender_id FK
        int receiver_id FK
        string status
        datetime requested_at
    }

  

    %% =========================
    %% RELATIONSHIPS
    %% =========================
    USER ||--o{ SNAP : "sends"}
    USER ||--o{ STORY : "creates"}
    SNAP ||--o{ SNAP_VIEW : "viewed_by"}
    STORY ||--o{ STORY_VIEW : "viewed_by"}
    USER ||--o{ FRIEND_REQUEST : "sent"}
    FRIEND_REQUEST |..|{ USER : "received"}

