package it.cnr.istc.stlab.testalod;

import org.apache.commons.configuration2.Configuration;
import org.apache.commons.configuration2.builder.fluent.Configurations;
import org.apache.commons.configuration2.ex.ConfigurationException;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;

public class TestaLODConfiguration {

	private static Logger logger = LogManager.getLogger(TestaLODConfiguration.class);
	private static TestaLODConfiguration instance;
	private int serverPort;

	private static String CONFIGURATION_FILE = "config.properties";

	private TestaLODConfiguration() {
		try {
			Configurations configs = new Configurations();
			Configuration config = configs.properties("config.properties");
			this.serverPort = config.getInt("serverPort");

			logger.info("Configuration file " + CONFIGURATION_FILE);
		} catch (ConfigurationException e) {
			e.printStackTrace();
		}
	}

	public static void setConfigFile(String file) {
		CONFIGURATION_FILE = file;
	}

	public static TestaLODConfiguration getPSSConfiguration() {
		if (instance == null) {
			instance = new TestaLODConfiguration();
		}
		return instance;
	}

	public int getServerPort() {
		return serverPort;
	}

}
