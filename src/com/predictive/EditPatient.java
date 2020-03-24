package com.predictive;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/EditPatient")
public class EditPatient extends HttpServlet{
	private static final long serialVersionUID = 1L;

	public EditPatient() {
		super();
	}
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	//Developed in iteration 4
	//Establish connection with mySQL to edit record
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);

		String firstname = request.getParameter("firstname");
		String lastname = request.getParameter("lastname");
		String address = request.getParameter("address");
		String department = request.getParameter("department");
		String prescription = request.getParameter("prescription");
		String id = request.getParameter("patientid");

		try {
			Class.forName("com.mysql.jdbc.Driver");
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/hospital", "root", "");
			Statement stmt = conn.createStatement();
			int i = stmt.executeUpdate(
					"UPDATE `patient` SET `patient_firstname` = '" + firstname + "'" + "," 
			+ "`patient_lastname` = '" + lastname + "'" + "," 
							+ "`address` = '" + address + "'" + "," 
			+ "`department` = '" + department + "'" + "," 
							+ "`prescription` = '" + prescription + "'" 
			+ "WHERE patient_id='" + id +"'");
			if (i > 0) {
				response.sendRedirect("patient.jsp");
			} else {
				response.sendRedirect("error.jsp");
			}
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
