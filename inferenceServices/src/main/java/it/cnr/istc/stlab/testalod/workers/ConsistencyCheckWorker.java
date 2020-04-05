package it.cnr.istc.stlab.testalod.workers;

import org.apache.jena.query.QueryExecution;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.NodeIterator;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;

import it.cnr.istc.stlab.testalod.resources.Utils;

public class ConsistencyCheckWorker {

	private String testCaseIRI;
	private Model model;

	private static final Logger logger = LogManager.getLogger(ConsistencyCheckWorker.class);

	public ConsistencyCheckWorker(String testCaseIRI) {
		super();
		this.testCaseIRI = testCaseIRI;
		this.model = ModelFactory.createDefaultModel();
	}

	public boolean run() throws TestALODException {
		RDFDataMgr.read(model, testCaseIRI);

		logger.trace("Number of triples in test case " + model.size());

		if (!checkDataInputType()) {
			throw new TestALODException("Consistency check test cases can be run only on SPARQL endpoints");
		}

		String sparqlEndpointURI = getSPARQLEndpointURI();
		logger.trace("SPARQL endpoint: "+sparqlEndpointURI);
		
		String sparqlQuery = getSPARQLQuery();
		logger.trace("SPARQL query: "+sparqlQuery);
		
		

		return false;
	}

	public boolean checkDataInputType() throws TestALODException {
		NodeIterator ni = model.listObjectsOfProperty(model.getResource(testCaseIRI),
				model.getProperty(Utils.TESTALOD_ONTOLOGY_PREFIX + "hasInputTestDataCategory"));

		if (!ni.hasNext()) {
			throw new TestALODException("No input data category declared");
		}

		String inputDataCategory = ni.next().asResource().getURI();
		logger.trace("Input Datata Category: " + inputDataCategory);

		return inputDataCategory.equals(Utils.SPARQLENDPOINT_DATACATEGORY)
				|| inputDataCategory.equals(Utils.SPARQLENDPOINT_DATACATEGORY_OLD);
	}

	public String getSPARQLEndpointURI() throws TestALODException {
		NodeIterator ni = model.listObjectsOfProperty(model.getResource(testCaseIRI),
				model.getProperty(Utils.TESTALOD_ONTOLOGY_PREFIX + "hasInputTestDataUri"));

		if (!ni.hasNext()) {
			throw new TestALODException("No SPARQL Endpoint declared");
		}
		return ni.next().asResource().getURI();
	}
	
	
	public String getSPARQLQuery() throws TestALODException {
		NodeIterator ni = model.listObjectsOfProperty(model.getResource(testCaseIRI),
				model.getProperty(Utils.TESTANNOTATIONSCHEMA_HASSPARQLQUERYUNITTEST));

		if (!ni.hasNext()) {
			throw new TestALODException("No SPARQL query unit test declared");
		}
		return ni.next().asLiteral().getString();
	}
	
	
	public static void main(String[] args) {
		ConsistencyCheckWorker ccw = new ConsistencyCheckWorker("https://w3id.org/arco/test/IC/testcase-01.owl");
		try {
			ccw.run();
		} catch (TestALODException e) {
			e.printStackTrace();
		}
	}

}
