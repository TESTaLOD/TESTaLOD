package it.cnr.istc.stlab.testalod.workers;

import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.Syntax;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.NodeIterator;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;

import it.cnr.istc.stlab.testalod.resources.Utils;

public class IntegrityConstraintCheckWorker {

	private String testCaseIRI;
	private Model model;

	private static final Logger logger = LogManager.getLogger(IntegrityConstraintCheckWorker.class);

	public IntegrityConstraintCheckWorker(String testCaseIRI) {
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
		logger.trace("SPARQL endpoint: " + sparqlEndpointURI);

		Query sparqlQuery = getSPARQLQuery();
		logger.trace("SPARQL query: " + sparqlQuery.toString(Syntax.syntaxSPARQL_11));

		boolean expectedResult = getExpectedResult();
		logger.trace("Expected result: " + expectedResult);

		QueryExecution qexec = QueryExecutionFactory.sparqlService(sparqlEndpointURI, sparqlQuery);

		return qexec.execAsk();
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

	public Query getSPARQLQuery() throws TestALODException {
		NodeIterator ni = model.listObjectsOfProperty(model.getResource(testCaseIRI),
				model.getProperty(Utils.TESTANNOTATIONSCHEMA_HASSPARQLQUERYUNITTEST));

		if (!ni.hasNext()) {
			throw new TestALODException("No SPARQL query unit test declared");
		}

		String sparqlQuery = ni.next().asLiteral().getString();

		Query q = QueryFactory.create(sparqlQuery);

		if (!q.isAskType()) {
			throw new TestALODException("Only ASK SPARQL query allowed");
		}

		return q;
	}

	public boolean getExpectedResult() throws TestALODException {
		NodeIterator ni = model.listObjectsOfProperty(model.getResource(testCaseIRI),
				model.getProperty(Utils.TESTANNOTATIONSCHEMA_HASEXPECTEDRESULT));

		if (!ni.hasNext()) {
			throw new TestALODException("No expected result declared");
		}

		return ni.next().asLiteral().getBoolean();

	}

	public static void main(String[] args) {
		IntegrityConstraintCheckWorker ccw = new IntegrityConstraintCheckWorker("https://w3id.org/arco/test/IC/testcase-01.owl");
		try {
			ccw.run();
		} catch (TestALODException e) {
			e.printStackTrace();
		}
	}

}
