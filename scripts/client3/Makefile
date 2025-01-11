SERVER1 = http://127.0.0.1:2137
SERVER2 = http://127.0.0.1:2138
SERVER3 = http://127.0.0.1:2139
SERVER4 = http://127.0.0.1:2140

SELLING_SHARES_PAYLOAD = '{"data": {"transaction_type": "SELLING_SHARES", "seller": "Alice", "buyer": "Bob", "shares": 50, "price": 100.0}}'
BUYING_SHARES_PAYLOAD   = '{"data": {"transaction_type": "BUYING_SHARES", "seller": "Alice", "buyer": "Bob", "shares": 50, "price": 100.0}}'
ISSUING_SHARES_PAYLOAD  = '{"data": {"transaction_type": "ISSUING_SHARES", "company": "Acme Corp", "shares": 1000, "price": 10.0}}'
GRANTING_SHARES_PAYLOAD = '{"data": {"transaction_type": "GRANTING_SHARES", "company": "Acme Corp", "grantee": "Charlie", "shares": 100}}'
INCREASING_CAPITAL_PAYLOAD = '{"data": {"transaction_type": "INCREASING_CAPITAL", "company": "Acme Corp", "additional_capital": 50000.0, "new_shares": 500}}'
PAYING_DIVIDENDS_PAYLOAD = '{"data": {"transaction_type": "PAYING_DIVIDENDS", "company": "Acme Corp", "shareholder": "Dana", "shares": 100, "dividend_per_share": 1.5}}'
VOTING_RESULTS_PAYLOAD = '{"data": {"transaction_type": "VOTING_RESULTS", "resolution_id": "res-123", "total_votes": 100, "votes_for": 60, "votes_against": 30, "votes_abstain": 10}}'

run:
	@echo "Uruchamianie serwera na porcie 2139..."
	python ../../app.py 2139

mine_block_sell:
	curl -X POST -H "Content-Type: application/json" \
	-d $(SELLING_SHARES_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_buy:
	curl -X POST -H "Content-Type: application/json" \
	-d $(BUYING_SHARES_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_issue:
	curl -X POST -H "Content-Type: application/json" \
	-d $(ISSUING_SHARES_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_grant:
	curl -X POST -H "Content-Type: application/json" \
	-d $(GRANTING_SHARES_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_increase:
	curl -X POST -H "Content-Type: application/json" \
	-d $(INCREASING_CAPITAL_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_dividends:
	curl -X POST -H "Content-Type: application/json" \
	-d $(PAYING_DIVIDENDS_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_voting:
	curl -X POST -H "Content-Type: application/json" \
	-d $(VOTING_RESULTS_PAYLOAD) \
	$(SERVER3)/mine_block

mine_block_sample: mine_block_sell mine_block_buy mine_block_issue

test: mine_block_sample register_node3_1

get_chain:
	curl $(SERVER3)/get_chain

sync_chain:
	curl $(SERVER3)/sync_chain

is_valid:
	curl $(SERVER3)/is_valid

peers:
	curl $(SERVER3)/peers

register_node3_1:
	curl -X POST -H "Content-Type: application/json" \
	-d '{"node_address": "$(SERVER1)"}' \
	$(SERVER3)/register_node

register_node3_2:
	curl -X POST -H "Content-Type: application/json" \
	-d '{"node_address": "$(SERVER2)"}' \
	$(SERVER3)/register_node

register_node3_4:
	curl -X POST -H "Content-Type: application/json" \
	-d '{"node_address": "$(SERVER4)"}' \
	$(SERVER3)/register_node

tamper_block:
	curl -X POST -H "Content-Type: application/json" \
	-d '{"block_index": 1, "new_data": "tampered data"}' \
	$(SERVER3)/tamper_block
