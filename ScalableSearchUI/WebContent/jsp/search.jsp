<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
	<title>Scalable Search</title>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css"/>
	<link rel="stylesheet" type="text/css" href="css/bootstrap-theme.min.css"/>
	<link rel="stylesheet" type="text/css" href="css/common.css"/>
	<link rel="stylesheet" type="text/css" href="css/search.css"/>
	
	<script type="text/javascript" src="js/jquery-3.1.1.min.js"></script>
	<script type="text/javascript" src="js/bootstrap.min.js"></script>
	<script type="text/javascript" src="js/search.js"></script>
</head>
<body>
<div class="header">
	<div class="row">
		<div class="col-md-8">
			Scalable Search
		</div>
	</div>
</div>
<div class="maincontent padding-top15">
		<div class="row">
			<div class="input-group">
		      <input type="text" class="form-control" placeholder="Enter Search Keywords..." id="txtSearch">
		      <span class="input-group-btn">
		        <button class="btn btn-default" type="button" id="btnSearch">
		        	<span class="glyphicon glyphicon-search" aria-hidden="true"></span>
		        </button>
		      </span>
		    </div>
		</div>
		<div class="row padding-top15 padding-bottom50" id="searchResults">
		
		</div>
		<div id="loadingImage" style="display: none">
			<img src="images/wait.gif" />
		</div>
</div>
<div class="footer navbar navbar-fixed-bottom">
	Copyright 2017 NCSU
</div>
</body>
</html>