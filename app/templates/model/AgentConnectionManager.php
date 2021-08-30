<?php
class AgentConnectionManager {
    public function getConnection() {        
        $dsn  = "mysql:host=localhost;dbname=agent";
        return new PDO($dsn, "root", "");  
    }
}
?>