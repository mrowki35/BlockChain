SERVER1 = http://127.0.0.1:5001
SERVER2 = http://127.0.0.1:5002

SELLING_SHARES_PAYLOAD = '{\"data\": {\"transaction_type\": \"SELLING_SHARES\", \"seller\": \"Alice\", \"buyer\": \"Bob\", \"shares\": 50, \"price\": 100.0}}'
BUYING_SHARES_PAYLOAD   = '{\"data\": {\"transaction_type\": \"BUYING_SHARES\", \"seller\": \"Alice\", \"buyer\": \"Bob\", \"shares\": 50, \"price\": 100.0}}'
ISSUING_SHARES_PAYLOAD  = '{\"data\": {\"transaction_type\": \"ISSUING_SHARES\", \"company\": \"Acme Corp\", \"shares\": 1000, \"price\": 10.0}}'
GRANTING_SHARES_PAYLOAD = '{\"data\": {\"transaction_type\": \"GRANTING_SHARES\", \"company\": \"Acme Corp\", \"grantee\": \"Charlie\", \"shares\": 100}}'
INCREASING_CAPITAL_PAYLOAD = '{\"data\": {\"transaction_type\": \"INCREASING_CAPITAL\", \"company\": \"Acme Corp\", \"additional_capital\": 50000.0, \"new_shares\": 500}}'
PAYING_DIVIDENDS_PAYLOAD = '{\"data\": {\"transaction_type\": \"PAYING_DIVIDENDS\", \"company\": \"Acme Corp\", \"shareholder\": \"Dana\", \"shares\": 100, \"dividend_per_share\": 1.5}}'
VOTING_RESULTS_PAYLOAD = '{\"data\": {\"transaction_type\": \"VOTING_RESULTS\", \"resolution_id\": \"res-123\", \"total_votes\": 100, \"votes_for\": 60, \"votes_against\": 30, \"votes_abstain\": 10}}'


#activate venv firstly run this:
# cd to this directory \Blockchain\scripts_windows\client1\
#	..\..\.venv\Scripts\activate

run:
	@echo "Uruchamianie serwera na porcie 5001..."
	python ../../app.py 5002

mine_block_sell:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(SELLING_SHARES_PAYLOAD)"

mine_block_buy:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(BUYING_SHARES_PAYLOAD)"

mine_block_issue:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(ISSUING_SHARES_PAYLOAD)"

mine_block_grant:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(GRANTING_SHARES_PAYLOAD)"

mine_block_increase:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(INCREASING_CAPITAL_PAYLOAD)"

mine_block_dividends:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(PAYING_DIVIDENDS_PAYLOAD)"

mine_block_voting:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/mine_block' -Method POST -ContentType 'application/json' -Body $(VOTING_RESULTS_PAYLOAD)"

mine_block_sample: mine_block_sell mine_block_buy mine_block_issue

test: mine_block_sample register_node1_2

get_chain:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/get_chain'"

sync_chain:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/sync_chain'"

is_valid:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/is_valid'"

peers:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/peers'"

register_node1_2:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/register_node' -Method POST -ContentType 'application/json' -Body '{\"node_address\": \"$(SERVER2)\"}'"

tamper_block:
	powershell -Command "Invoke-RestMethod -Uri '$(SERVER2)/tamper_block' -Method POST -ContentType 'application/json' -Body '{\"block_index\": 1, \"new_data\": \"tampered data\"}'"
