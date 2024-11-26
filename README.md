# Assignment 1
## Deadline: <span style="color:red;">14.04.2024, 23:00</span>

--- 

# PaperBack: A Newspaper Subscription Management Software

Let us imagine, that we are building up an application to manage newspaper subscriptions.
The software shall be used by employees of the newspaper agency to manage the newspaper 
issues and monitor their client subscriptions.
This programming task is about implementing a web API, so that the same software can be
customized by different newspaper agencies to build their own applications based on the provided API. 
At the moment, we do not care about the front-end of the application, which could be 
any browser or a mobile app. And we also don’t care about a database that stores the data 
persistently. In this exercise, we deal with the API implementation only. 
You may use a REST client like Postman to quickly see the results of the API call. 
It is recommended to use Python requests library and Pytest to thoroughly test the API. 
A Swagger based UI is provided, so that you can also test the application based on a 
browser front-end. Design your objects and classes allowing for easy future extensions.

## Functionality

The API consists of the following main functionality

**Management of newspapers and issues**
- Add/remove/update a new newspaper. Each paper has a (unique) paper ID, name, issue frequency (in days), and monthly price
- Add/remove/update an issue of a newspaper. Each issue has a publication date, number of pages, etc
- Each issue has an editor (i.e. the responsible person; see below)
- Initially, paper issues are not published, but once updated, they can be delivered to subscribers

**Management of editors**
- Add/remove/update editors to/from the system. Each editor has a (unique) editor-id, name, address and a list of newspapers, s/he can work for care of.
- When an editor is removed (e.g., quits the job), transfer all issues in his/her supervision to another editor of the same newspaper.

**Management of subscribers**
- Add/remove subscribers to/from the system. Each subscriber has a (unique) subscriber ID, name, address and a list of newspapers that they are subscribed to.
- Each client can choose to subscribe to special issues
- When a client is removed (e.g., cancels a subscription), all subscriptions are stopped



If you have a fix for a problem, feel free to leave a Pull Request. 
([Helpful Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request))
