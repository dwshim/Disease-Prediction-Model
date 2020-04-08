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

import javax.servlet.RequestDispatcher;
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
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	//Developed in iteration 5
	//Establishing connection with flask server and retrieve response from the server as json
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);

		String bmi = request.getParameter("bmi");
		String pregnancies = request.getParameter("pregnancies");
		String glucose = request.getParameter("glucose");
		String bp = request.getParameter("bp");
		String pedigree = request.getParameter("pedigree");
		String output = "";

		String query_url = "http://localhost:12347/predict";
		String json = "[{\"area_worst\": " + pregnancies + ", \"radius_worst\": " + glucose + ", \"perimeter_worst\": " + bp + ", \"concave points_mean\": " + bmi + ", \"concave points_worst\": " + pedigree + "}]";
		
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
			JSONObject myResponse = new JSONObject(result);
			request.setAttribute("result", myResponse.getString("prediction"));
			request.setAttribute("area_worst", pregnancies);
			request.setAttribute("radius_worst", glucose);
			request.setAttribute("perimeter_worst", bp);
			request.setAttribute("concave_points_mean", bmi);
			request.setAttribute("concave_points_worst", pedigree);
			request.getRequestDispatcher("predictor.jsp").forward(request, response);
			in.close();
			conn.disconnect();
			if (myResponse.getString("prediction") != null){
				if (myResponse.getString("prediction").equals("[1]")) {
					output = "Malignant";
					} else if (myResponse.getString("prediction").equals("[0]")) {
						output = "benign";
					} 
				}
		} catch (Exception e) {
			System.out.println(e);
		}
		
		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://" + DatabaseInfo.DB_URL + "/" + DatabaseInfo.DB_NAME + "", DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS); 
			Statement stmt = conn.createStatement();
			int i = stmt.executeUpdate(
					"INSERT INTO `prediction`(`concave_points_mean`, `radius_worst`, `perimeter_worst`, `area_worst`, `concave_points_worst`, `result`) VALUES ('"
							+ bmi + "','" + glucose + "','" + bp + "','" + pregnancies + "','" + pedigree + "','" + output
							+ "')");
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}