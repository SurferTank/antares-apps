#Message exchange format

In order to use the message infrastructure to receive documents, the following structure has to be followed. 

example:
```json
{
        "documents": [
			{
				"type": "account_form", 
	    			"post_date": "2001-01-01T00:00:00+3",
	     		"create_summary": false,
				"header": [
					{
						"period": 2001
					}
				],
			"fields": [
				{
					"an_amount": 100.1
				}
			]
			}
		]
}
```
