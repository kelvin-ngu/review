### Create Room & Add Room Members

To add moderators + reviewers + reviewees to a specific room.

* Route: `/rooms/`
* Method: POST
* Body (JSON):
    ```
    {
        room: [
            uuid (room_id),
            uuid
        ]
        members : [
            {
                moderators: [{
                    id: uuid (moderator_id)
                    added_by: 
                }]

                reviewers: [{
                    id: uuid (reviewer_id)
                    added_by: 
                }]

                direct_reviewees: [{
                    id: uuid (direct_reviewee_id)
                    added_by:
                }]

                indirect_reviewees:[{
                    id: uuid (indirect_reviewee_id)
                    added_by:
                }]
            }
        ]
    }

* Return:
    ```
    {
        
    }
    ```