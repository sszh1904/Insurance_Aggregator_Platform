<?php
class CustomerConnectionManager {
    public function getConnection() {        
        $dsn  = "mysql:host=localhost;dbname=customer";
        return new PDO($dsn, "root", "");  
    }
}
?>