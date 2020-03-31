package com.predictive;
import java.io.IOException;
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

@WebServlet("/DeletePatient")
public class DeletePatient extends HttpServlet{
	
	private static final long serialVersionUID = 1L;

	public DeletePatient() {
		super();
	}
	
	//Developed in iteration 3
	//Establish connection with mySQL to delete record
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
String id = request.getParameter("id").toString();
		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://" + DatabaseInfo.DB_URL + "/" + DatabaseInfo.DB_NAME + "", DatabaseInfo.DB_USERNAME, DatabaseInfo.DB_PASS); 
			Statement stmt = conn.createStatement();
			Statement stmt2 = conn.createStatement();
			int j = stmt2.executeUpdate(
					"DELETE FROM `patient_data` WHERE patient_id = '" + id + "'");
			int i = stmt.executeUpdate(
					"DELETE FROM `patient` WHERE patient_id = '" + id + "'");
			if (i > 0 || j >0) {
				response.sendRedirect("patient.jsp");
			} else {
				response.sendRedirect("error.jsp");
			}
			conn.close();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		
	}
}
