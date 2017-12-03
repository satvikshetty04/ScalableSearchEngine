package com.dic.search.controller;

import java.io.InputStream;
import java.io.StringWriter;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.io.IOUtils;
import org.apache.struts2.ServletActionContext;
import org.json.JSONArray;
import org.json.JSONObject;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.opensymphony.xwork2.ActionSupport;

public class SearchAction extends ActionSupport{
	private static final long serialVersionUID = 1L;
	
	private String actionName;
	private String jsonString;
	private String queryString;
	
	public String execute() throws Exception {
		
		HashMap<String, Object> returnData = new HashMap<String, Object>();
		
		//HttpServletRequest request = ServletActionContext.getRequest();
		
		String url = "https://search-newssearchengine-rhlbiq3mtga7gj6czbw3box4km.us-east-1.es.amazonaws.com/news/news/_search?q="+queryString;
		
		if(actionName.equals("ACTION_SEARCH_ES"))
		{
			InputStream input = new URL(url).openStream();
			StringWriter writer = new StringWriter();
			IOUtils.copy(input, writer, "UTF-8");
			
			String jsonResult = writer.toString();
			
			JSONObject js = new JSONObject(jsonResult);
			JSONArray resultArray = js.getJSONObject("hits")
							 .getJSONArray("hits");
			System.out.println(resultArray.toString(2));
			
			ArrayList<String []> articleDetails = new ArrayList<String []>();
			
			for(int i=0;i<resultArray.length();i++)
			{
				JSONObject articleJSON = resultArray.getJSONObject(i)
								  			.getJSONObject("_source");
				
				InputStream articleInput = new URL(articleJSON.getString("link"))
													.openStream();
				
				StringWriter strWriter = new StringWriter();
				IOUtils.copy(articleInput, strWriter, "UTF-8");
				
				String articleText = strWriter.toString();
				
				String [] article = {articleJSON.getString("category"), articleText};
				
				articleDetails.add(article);
			}
			returnData.put("articleList", articleDetails);
		}
		
		Gson gson = new GsonBuilder().create();
		setJsonString(gson.toJson(returnData));

		return SUCCESS;
	}

	public String getActionName() {
		return actionName;
	}

	public void setActionName(String actionName) {
		this.actionName = actionName;
	}

	public String getJsonString() {
		return jsonString;
	}

	public void setJsonString(String jsonString) {
		this.jsonString = jsonString;
	}

	public String getQueryString() {
		return queryString;
	}

	public void setQueryString(String queryString) {
		this.queryString = queryString;
	}
	
	
}
