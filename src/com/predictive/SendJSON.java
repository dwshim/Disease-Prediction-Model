package com.predictive;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.commons.io.IOUtils;
import org.json.JSONObject;

@WebServlet("/SendJSON")
public class SendJSON extends HttpServlet {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public SendJSON() {
		super();
		// TODO Auto-generated constructor stub
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);

		String bmi = request.getParameter("bmi");
		String pregnancies = request.getParameter("pregnancies");
		String glucose = request.getParameter("glucose");
		String bp = request.getParameter("bp");
		String pedigree = request.getParameter("pedigree");

		String query_url = "http://localhost:12347/predict";
		String json = "{\"Pregnancies\": " + pregnancies + ", \"Glucose\": " + glucose + ", \"BloodPressure\": " + bp + ", \"BMI\": " + bmi + ", \"DiabetesPedigreeFunction\": " + pedigree + "}";
		
		try {
			URL url = new URL(query_url);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setConnectTimeout(5000);
			conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
			conn.setDoOutput(true);
			conn.setDoInput(true);
			conn.setRequestMethod("POST");
			OutputStream os = conn.getOutputStream();
			os.write(json.getBytes("UTF-8"));
			os.close();
			
			// read the response
			InputStream in = new BufferedInputStream(conn.getInputStream());
			String result = IOUtils.toString(in, "UTF-8");
			System.out.println(result);
			System.out.println("result after Reading JSON Response");
			JSONObject myResponse = new JSONObject(result);
			System.out.println("jsonrpc- " + myResponse.getString("jsonrpc"));
			System.out.println("id- " + myResponse.getInt("id"));
			System.out.println("result- " + myResponse.getString("result"));
			in.close();
			conn.disconnect();
		} catch (Exception e) {
			System.out.println(e);
		}
	}
}