package it.cnr.istc.stlab.testalod.resources;

import java.io.ByteArrayOutputStream;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.Response;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;

@Path("/consistencyCheck")
public class ConsistencyCheck {

	private static final Logger logger = LogManager.getLogger(ConsistencyCheck.class);

	@GET
	@Produces("application/rdf+xml")
	public Response consistencyCheck(@QueryParam("IRI") String iri) {

		logger.trace("Checking consistency of " + iri);

		Model m;
		try {
			if (Utils.checkConsistency(iri)) {
				m = getTrue(iri);
			} else {
				m = getFalse(iri);
			}
			ByteArrayOutputStream bos = new ByteArrayOutputStream();
			m.write(bos, "RDF/XML");
			return Response.ok(bos.toString()).build();
		} catch (OWLOntologyCreationException e) {
			e.printStackTrace();
		}
		return Response.serverError().build();
	}

	private static Model getFalse(String iri) {
		Model m = ModelFactory.createDefaultModel();
		m.addLiteral(m.createResource(iri),
				m.createProperty(
						"http://www.ontologydesignpatterns.org/schemas/testannotationschema.owl#hasActualResult"),
				false);
		return m;
	}

	private static Model getTrue(String iri) {
		Model m = ModelFactory.createDefaultModel();
		m.addLiteral(m.createResource(iri),
				m.createProperty(
						"http://www.ontologydesignpatterns.org/schemas/testannotationschema.owl#hasActualResult"),
				true);
		return m;
	}

}
