# user api documentation

1. /users/register/
    -allowed method - POST with data (username, email, password), response with messange "User successfully created" and conformation mail will be recieved in user's email, then user can conform their email by clicking the recieved link 
    ![user-register](https://user-images.githubusercontent.com/85220975/174128610-37bae9b8-6ad1-4eaa-bafa-4ea51708dc42.png)
    
2. /users/login/
    -allowed method - POST with data (email, password), response with (access_token, refresh_token) if user is exit and password is correct
    ![user-login](https://user-images.githubusercontent.com/85220975/174128366-3b74867c-d2e4-44b5-a841-b649fa64fb89.png)

3. /users/reset_password/
    -allowed method - POST with Authentication token, response with message "Reset Password Email Sent" verification mail will be recieved in user's email, then user can conform password reset by clicking the recieved link 
    ![reset-password](https://user-images.githubusercontent.com/85220975/174128735-5e777d49-c7e6-4905-8968-2e5beb14081f.png)

4. /users/change_password/
    -allowed method - POST with Authentication token with data (password, new_password, confirm_password), response with message "Password changed successfully" 
    ![change-password](https://user-images.githubusercontent.com/85220975/174128812-3c0374b6-babd-4607-bcab-74b07be97b27.png)

5. /users/forgot_password/
    -allowed method - POST with Authentication token with data (new_password, confirm_password), response with message "Password saved successfully"
    ![forget-password](https://user-images.githubusercontent.com/85220975/174128864-159db54f-929f-47e3-95d8-aa64afef23d2.png)

6. /users/developer/
    -allowed method - GET with Authentication token, response with the users list related to the authenticated user
    ![developer-list](https://user-images.githubusercontent.com/85220975/174129242-45142958-713e-4c1c-9930-ca4d36048202.png)

7. /users/developer/{id}/
    -allowed method - DELETE with Authentication token, response with success message
    ![delete-developer](https://user-images.githubusercontent.com/85220975/174129300-307eec44-e8e7-4627-8e8c-41dedcb86f37.png)

8. /users/get_user_activites/
    -allowed method - GET with Authentication token, response with the users activities list related to the authenticated user
    ![get_user_activites](https://user-images.githubusercontent.com/85220975/174129367-2a3410c5-b128-46ae-8ff7-02c0ebc3b0c7.png)

9. /users/get_hashed_id/
    -allowed method - GET with Authentication token, response with "hashed_id"
    ![get_hashed_id](https://user-images.githubusercontent.com/85220975/174128944-a2ed286a-2ed4-4366-8706-36252a339336.png)

10. /users/subscribe/
    -allowed method - POST with data (uid as username, secret as payment secret recived from payment_intent), response with "user subscription created."

11. /users/payment_intent/
    -allowed method - POST with data (subscription as subscription type), response with message "payment intent created" and payment secret

12. /users/profile/{id}/
    -allowed method - GET, response with detail of the user of passed id in url
    ![user-get](https://user-images.githubusercontent.com/85220975/175867311-e3b1148f-7c6f-4e58-88f5-fd3ef482761c.png)

    -PUT with Authentication token, and data field you want to update, response with updated user instance
    ![user-update](https://user-images.githubusercontent.com/85220975/175867366-a67d07c0-e226-4f61-bd7d-92d76f0fd582.png)



# AI api documentation

1. /ai/
    -allowed method - GET, response with list of basedevices
    ![ai-list](https://user-images.githubusercontent.com/85220975/176168482-3fdeec6c-286d-4443-845e-11fdc4b4e91e.png)

    - POST with Authentication token and required fields (screenshots - image files, user - user email, title - title of device) and other extra fields (type - 1 for android and 2 for ios, cover_image and demo both are filefields, reviews - id of existing reviews), response with new created device object as we passed in request
    ![ai-post](https://user-images.githubusercontent.com/85220975/174577835-e9387085-3390-4b82-bfcf-9bfa42d410f9.png)

2. /ai/{id}/
    -allowed method - GET, response with detail of passed id's BaseDevice
    ![ai-detail](https://user-images.githubusercontent.com/85220975/176168560-da2b9960-cf82-4640-8e94-47c0fd9cc796.png)

    - PUT with Authentication token and fields same as POST method but for screenshots give the previous mediafile id and new image file if you want to add screenshot but to delete some screenshots from previous leave that id in previous screenshots, response with updated instance of passed id
    ![ai-put](https://user-images.githubusercontent.com/85220975/174577946-36788bcf-cea7-4f36-96e0-0c3a67425b20.png)

    -DELETE with Authentication token, response with status 204 no content 
    ![ai-delete](https://user-images.githubusercontent.com/85220975/174578072-41ec1dd0-92a5-4f13-8531-d165f0f30250.png)

3. /ai/review/{id- id of basedevice object}/
    -allowed method - POST with authentication token and data (title, description, rating), response with success message
    ![ai-review-post](https://user-images.githubusercontent.com/85220975/174582734-5ee13efe-444a-41f5-93d8-efe040145317.png)

4. /ai/review/{id- id of review object}/
    -PATCH with authentication token and data (title, description, rating), response with success message
    ![ai-review-patch](https://user-images.githubusercontent.com/85220975/174583429-c0f2e11c-b625-4d94-a32d-1587190f9584.png)

    -DELETE with Authentication token, response with status 204 no content
    ![ai-review-delete](https://user-images.githubusercontent.com/85220975/176168646-27df36ec-0dab-4ce6-83d2-335e466e7fc6.png)
    

5. /ai/publish/{id- device id}/
    -allowed method - POST with authentication token, response with sucess message if the requesting user is related admin of device's user
    ![ai-publish-id](https://user-images.githubusercontent.com/85220975/174586211-bdf29461-fde0-4a95-b61f-f86d55f7cf8a.png)

6. /ai/media/{id}/
    -allowed method - GET, response with media instance of passed id
    ![media-get](https://user-images.githubusercontent.com/85220975/175867562-fabaed9a-16de-4a00-ab31-e172f31cef29.png)


# Block api documentation

1. /block/
    -allowed method - GET, response with list of blocks
    ![block-list](https://user-images.githubusercontent.com/85220975/176168725-4cdcfd13-a85c-4ec7-a316-b1e3a6d131bf.png)

    - POST with Authentication token and required fields (screenshots - image files, user - user email, title - title of block) and other extra fields (description_block, cover_image and demo both are filefields, reviews - id of existing reviews), response with new created block object as we passed in request
    ![block-post](https://user-images.githubusercontent.com/85220975/174591272-a1d181da-6575-42db-98ef-9cd7de4fb165.png)

2. /block/{id}/
    -allowed method - GET, response with detail of passed id's BaseDevice
    ![block-detail](https://user-images.githubusercontent.com/85220975/176168822-cda05c48-266d-481d-93a5-018db2de3a31.png)

    - PUT with Authentication token and fields same as POST method but for screenshots give the previous mediafile id and new image file if you want to add screenshot but to delete some screenshots from previous leave that id in previous screenshots, response with updated instance of passed id
    ![block-id-put](https://user-images.githubusercontent.com/85220975/174592096-0cc48b84-e23e-4875-8d38-7fbd926258a0.png)

    -DELETE with Authentication token, response with status 204 no content 
    ![block-id-delete](https://user-images.githubusercontent.com/85220975/174592370-5db73233-c6c1-43b6-81b8-5678c254cde0.png)

3. /block/review/{id- id of block object}/
    -allowed method - POST with authentication token and data (title, description, rating), response with success message
    ![block-review-post](https://user-images.githubusercontent.com/85220975/174592969-72283ee6-db0d-45d5-8571-ea8bda18d98c.png)

4. /block/review/{id- id of review object}/
    -PATCH with authentication token and data (title, description, rating), response with success message
    ![block-review-patch](https://user-images.githubusercontent.com/85220975/174593327-c6d0642e-c9ab-4d87-b97f-048a8318c07c.png)

    -DELETE with Authentication token, response with status 204 no content
    ![block-review-delete](https://user-images.githubusercontent.com/85220975/176168891-64f07beb-f08f-46d7-9d44-81067860fd79.png)

# Extension api documentation

1. /extensions/
    -allowed method - GET, response with list of extensions
    ![extension-list](https://user-images.githubusercontent.com/85220975/176168998-8bc6557d-3495-42bf-80e4-5f6e2ca9c18f.png)

    - POST with Authentication token and required fields (screenshots - image files, user - user email, title - title of extension) and other extra fields (description, cover_image and demo both are filefields, reviews - id of existing reviews), response with new created block object as we passed in request
    ![extension-post](https://user-images.githubusercontent.com/85220975/174604364-b6302b7b-d48c-4891-822b-e4c4437b3fc4.png)

2. /extensions/{id}/
    -allowed method - GET, response with detail of passed id's Extension
    ![extension-detail](https://user-images.githubusercontent.com/85220975/176169072-e80b3dc2-100b-4b8f-b327-6ab935515d90.png)

    - PUT with Authentication token and fields same as POST method but for screenshots give the previous mediafile id and new image file if you want to add screenshot but to delete some screenshots from previous leave that id in previous screenshots, response with updated instance of passed id
    ![extension-id-put](https://user-images.githubusercontent.com/85220975/174605051-6ebeb0f3-3d88-444f-859b-dc8abc25fd8c.png)

    -DELETE with Authentication token, response with status 204 no content 
    ![extension-id-delete](https://user-images.githubusercontent.com/85220975/174605259-00799819-50ce-46c6-abf4-455afe821242.png)

3. /extensions/review/{id- id of extension object}/
    -allowed method - POST with authentication token and data (title, description, rating), response with success message
    ![extension-review-post](https://user-images.githubusercontent.com/85220975/174605549-30ea4cc1-d41f-4d8e-9bb6-0dedc7c5bafe.png)

4. /extensions/review/{id- id of review object}/
    -PATCH with authentication token and data (title, description, rating), response with success message
    ![extension-review-patch](https://user-images.githubusercontent.com/85220975/174606032-c07becaf-0ad0-4cc6-88ac-607052f019af.png)

    -DELETE with Authentication token, response with status 204 no content
    ![extension-review-delete](https://user-images.githubusercontent.com/85220975/176169135-36de1d0e-c562-4d45-8be0-d5529ba57cc6.png)
