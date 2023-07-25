### Create Room & Add Room Members

To add moderators + reviewers + reviewees to a specific room.

* Route: `/rooms/`
* Method: POST
* Body (JSON):
    ```
    {
    "title": str,
    "description": str,
    "year": int,
    "created_by": id,       #user_id
    "moderators": [
        id, id, id          #list of user_ids
        ],
    "added_by": 
        id                  #user_id
    }
    

* Return:
    ```
    {
    # Room objects
    "room": {
        "id": uuid (room_id),
        "title": str,
        "description": str,
        "year": int,
        "closed_at": datetime or null,
        "status": status_option,
        "created_by": {
            "id": user_id,
            "username": str,
            "is_exec": boolean,
            "email": email_field
        },
        "created_at": datetime,

        "moderators_by_room": [
            moderator_id,
            moderator_id
        ],
        "reviewers_by_room": [],
        "direct_reviewees_by_room": [],
        "indirect_reviewees_by_room": [],

        # Moderator objects
        "moderators": [
            {
                "id": 1,
                "username": "kelvin",
                "is_exec": true,
                "email": "kelvin@email.com"
            },
            {
                "id": 2,
                "username": "samuel",
                "is_exec": true,
                "email": "samuel@email.com"
            }
        ]

        # and also Reviewer, Direct Reviewee, Indirect Reviewee Objects 
    }
}
    ```