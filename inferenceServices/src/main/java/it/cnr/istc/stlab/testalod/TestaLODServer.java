package it.cnr.istc.stlab.testalod;

import java.io.IOException;
import java.util.EnumSet;

import javax.servlet.DispatcherType;

import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.FilterHolder;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.servlets.CrossOriginFilter;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;

public class TestaLODServer {

	private static Logger logger = LogManager.getLogger(TestaLODServer.class);

	public static void main(String[] args) throws JsonParseException, JsonMappingException, IOException {

		if (args.length > 0) {
			logger.info("Configuration File " + args[0]);
			TestaLODConfiguration.setConfigFile(args[0]);
		}

		int port = TestaLODConfiguration.getPSSConfiguration().getServerPort();

		// Jetty server
		Server jettyServer = new Server(port);

		// Main context handler
		ServletContextHandler servletContextHandler = new ServletContextHandler(ServletContextHandler.SESSIONS);
		servletContextHandler.setContextPath("/");

		// Add the filter, and then use the provided FilterHolder to configure it
		// Enable cross site requests
		FilterHolder cors = servletContextHandler.addFilter(CrossOriginFilter.class, "/*",
				EnumSet.of(DispatcherType.REQUEST));
		cors.setInitParameter(CrossOriginFilter.ALLOWED_ORIGINS_PARAM, "*");
		cors.setInitParameter(CrossOriginFilter.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*");
		cors.setInitParameter(CrossOriginFilter.ALLOWED_METHODS_PARAM, "GET,POST,HEAD");
		cors.setInitParameter(CrossOriginFilter.ALLOWED_HEADERS_PARAM, "X-Requested-With,Content-Type,Accept,Origin");

		ServletHolder servletHolder = servletContextHandler
				.addServlet(org.glassfish.jersey.servlet.ServletContainer.class, "/*");
		servletHolder.setInitOrder(1);
		servletHolder.setInitParameter("jersey.config.server.provider.packages",
				"it.cnr.istc.stlab.testalod.resources");
		servletHolder.setInitParameter("com.sun.jersey.api.json.POJOMappingFeature", "true");
		servletHolder.setInitParameter("jersey.config.server.wadl.disableWadl", "true");
		servletHolder.setInitParameter("jersey.config.server.provider.classnames",
				"org.glassfish.jersey.jackson.JacksonFeature");

		logger.info(" will be available at " + "http://localhost:" + port + "/*");

		// add main context to Jetty
		jettyServer.setHandler(servletContextHandler);

		logger.trace("Handler set");

		try {
			jettyServer.start();
			logger.info("Done! Jetty Server is up and running!");
			jettyServer.join();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				jettyServer.destroy();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

}
