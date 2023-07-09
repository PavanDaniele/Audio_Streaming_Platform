# Audio_Streaming_Platform

## Project Description

The project is based on creating a web application that provides a digital music service similar to the more famous 'Spotify' platform.

The web application, called 'Unify', interfaces with an underlying SQL database designed specifically for this purpose and integrated using libraries from Flask and SQLAlchemy in the Python language.

PostgreSQL was chosen as the DBMS, and pgadmin was chosen to communicate with the database.

- [Autentication](#Autentication)
- [Statistic](#Statistic)
- [Logical & Physical model design](#Logical-&-Physical-model-design)
- [Sample queries to populate the database](#Sampl-queries-to-populate-the-database)

## Autentication
Upon registration, each user can decide whether to create a "Listener" or "Artist" account. Both profiles can create playlists to group, for example, favorite songs, but users who register with the "Artist" account are entitled to additional features such as:
- creating songs to include in any album or to leave as singles.
- access to an analytical interface that allows you to consult statistical data on your songs, albums, and playlists.

### Here are some screenshots
Authentication (login with e-mail and password) is required to use Unify; the following interface is presented:
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/6b25fce4-cb5e-4fb8-8f3a-548f706e8cda)

![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/f582442c-05ea-46bc-aaed-32701fa14470)



However, if you don't have an account, you must create one.
### Create an account
When creating an account, you are asked for the type of profile you want to use:
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/8936c4e9-78dc-41b4-8314-6bcf66bc73a8)

Later, you are asked contacts and personal information:
If you're a Listener:
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/88a2f289-2943-4e99-aba7-beba60d5b970)

If you're an Artist:
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/27bfc8e4-8473-4c06-8afc-3be539e94215)

## Statistics
This special area shows, in the form of a bar chart, statistics related to listening to a particular song, artist, rather than a playlist or genre of music (Type).
The image below shows the Statistics page:
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/3f396d62-4a90-49fc-bd85-26891ed16293)

## Logical & Physical model design
- ### Logical model design
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/0d3f856f-648f-4aed-b84b-578753636d58)

- ### Physical model design
![image](https://github.com/PavanDaniele/Audio_Streaming_Platform/assets/127297363/79ff7217-a1fb-4536-8453-e91fdeed1baa)

In the logical (relational) schema there are all the classes with their appropriately chosen attributes.

Within the schema there is a single hierarchy of classes: the **Users** class represents the people who make up our universe of interest and specifies some of their personal data and contact information. It has a subclass **Artist**s, and vertical partitioning is used without adding additional attributes, since all useful information is already present directly within the **Users** class. Both of these classes represent the people actually already registered within the application.

The **Songs** class contains all the information about the songs present, in particular their title, duration and publication date, and is connected via an association to the **Artists** class (since that type of user has the ability to add songs).

The **Playlist** class represents the various "collections of songs," e.g., favorite songs, that any user can create therefore this class is joined to both **Users** and **Songs**. A Playlist can be private or public; its creation date is also stored.

The **Album** table identifies the various albums uploaded by artists, it has as attributes: the album title and its release date. It is also linked with the **Songs** class.

The primary purpose of the web app is to act as an audio streaming platform, so the ability for any user to listen to any song is necessary. In the association between Users and Songs, it was deemed appropriate to add a Listen table that would group information such as the number of times a particular song is listened to and the date of the last listen. These attributes will be useful for implementing listening statistics.

## Sample queries to populate the database
