# 4111chocolate

psql account: yy2738, password: 0744

URL: 35.185.33.176:8111

Description:
Our proposal from part 1 said that our web app would make it simple for the shop managers to filter their stock by various qualities, to make it easy for them to update their stock, and to make it easy for them to contact their suppliers. We implemented all of these things, but we implemented filters for qualities different from the ones we initially mentioned, and the updating capabilities we implemented were limited.

In our inventory web app, the manager is provided an overview of several aspects of the business: information on how many chocolates are stocked and what needs to be reordered (stock and reorders), information about the chocolates stocked (inventory), profit and revenue, and customers' orders. 


2 most interesting web pages:
index.html
This page is interesting because it automatically displays the result of many queries to give the manager an overview of how the shop is doing. It also contains many interactive queries where the manager can type input into a text box, select a value from a drop down list, etc, and then see the result of the query.
The page is divided into 4 sections: stock and reorders, inventory, profit and revenue, and orders.

In the stock and reorders section, manager can check how many chocolates the shop has by inputting the specific chocolate id. The page also automatically shows, for chocolates where the number on hand is less than 20, the detailed chocolate information and contact information of the company that produces it. Also, the manager can type specific chocolate id to see the company information of the company that produces that chocolate. Lastly, the manager can update the reorder number for one specific chocolate. 
In the inventory section, manager can check the detailed chocolate information by choosing the type of the chocolate from a drop down list. In addition, manager can easily know what chocolate to recommend, if customer desires a chocolate which made by the cocoa beans from specific country. 
In the profit and revenue section, manager can find out what the most popular chocolate or the least popoular chocolate in the shop is by using a checkbox. Also, the system will show what is the shop's total profit so far and the average revenue per order automatically.
In the order management section, system will show the order history, and the detailed information for those orders whose delivery have not been completed yet. Also, the manager can check the order information of a specific order by typing in its order number. Last but not least, manager can find the order placed on one specific date by inputting the date in the MM/DD/YY date format.

bpopular.html
This page displays the most and least popular chocolates, and it is interesting because we have to make multiple database queries to get that information.
(This is the results page of a query. The only page that takes inputs for queries is the index.html page, and the various interesting queries on it are described above.)