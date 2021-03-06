Feature: Query inventory Computers
    I want to be able to query inventory computers

    Background: Test POST /inventory/computers/query
      Given the account is an authorized tenant
      And the inventory_computers client URL is /inventory/computers

    # /inventory/computers/query
    @positive @p0 @smoke
    Scenario Outline: Query inventory Computers
        Given I have query details in <filename> for entities using the inventory_computers api
        When I get the query_results from a query of inventory_computers
        Then the inventory_computers response status is 200 OK
        And the response contains a list of inventory_computers
        And the inventory_computers entities in the response contain the data from <filename>

        Examples: Filenames
        | filename              |
        | active_rpc_port.json  |
        | active_ping_port.json |

    # /inventory/computers/query - not local
    @positive @p0 @smoke
    @not-local
    Scenario Outline: Query inventory Computers not local
        Given I have query details in <filename> for entities using the inventory_computers api
        When I get the query_results from a query of inventory_computers
        Then the inventory_computers response status is 200 OK
        And the response contains a list of inventory_computers
        And the inventory_computers entities in the response contain the data from <filename>

        Examples: Filenames
        | filename              |
        | dmi_sys_vendor.json   |
        | mem_Dirty.json        |

    # /inventory/computers/query - params
    @positive @p0
    Scenario Outline: Query Inventory Computers parameters
        Given I have query details in <query_filename> for entities using the inventory_computers api
        When I get with parameters in <param_filename> the query_results from a query of inventory_computers
        Then the inventory_computers response status is 200 OK
        And the response contains a list of inventory_computers
        And url parameters to the inventory_computers api are applied
        And the inventory_computers entities in the response contain the data from <filename>

        Examples: Fields
        | query_filename              | param_filename            |
        | active_rpc_port.json        | typical_query_params.json |
        | active_ping_port.json       | typical_query_params.json |

    # /inventory/computers/query - params - not local
    @positive @p0
    @not-local
    Scenario Outline: Query Inventory Computers parameters not local
        Given I have query details in <query_filename> for entities using the inventory_computers api
        When I get with parameters in <param_filename> the query_results from a query of inventory_computers
        Then the inventory_computers response status is 200 OK
        And the response contains a list of inventory_computers
        And url parameters to the inventory_computers api are applied
        And the inventory_computers entities in the response contain the data from <filename>

        Examples: Fields
        | query_filename              | param_filename            |
        | dmi_sys_vendor.json         | typical_query_params.json |
        | mem_Dirty.json              | typical_query_params.json |

    # /inventory/computers/query - offset_id
    @positive @p0
    @offset @not-local
    Scenario Outline: Query Inventory Computers parameters and test the offset_id param
        Given I have query details in <query_filename> for entities using the inventory_computers api
        When I get with parameters in <param_filename> the query_results from a query of inventory_computers
        Then I get with offset parameters in <second_few> the query_results from a query of inventory_computers
        Then the inventory_computers response status is 200 OK
        And the response contains an offset list of inventory_computers that have been offset by the offset_id
        And the inventory_computers entities in the response contain the data from <filename>

        Examples: Fields
        | query_filename              | param_filename | second_few |
        | active_rpc_port.json        | first_ten.json | next_five.json |
        | active_ping_port.json       | first_ten.json | next_five.json |

        # TODO negative testing
