package it.cnr.istc.stlab.testalod.resources;

import java.io.ByteArrayOutputStream;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.Response;

import org.apache.jena.rdf.model.Model;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;

import it.cnr.istc.stlab.testalod.workers.IntegrityConstraintCheckWorker;
import it.cnr.istc.stlab.testalod.workers.TestALODException;

@Path("/integrityConstraintCheck")
public class IntegrityConstraintCheck {

	private static final Logger logger = LogManager.getLogger(IntegrityConstraintCheck.class);

	@GET
	@Produces("application/rdf+xml")
	public Response consistencyCheck(@QueryParam("IRI") String iri) {

		logger.trace("Integrity constraint check " + iri);

		try {
			IntegrityConstraintCheckWorker iccw = new IntegrityConstraintCheckWorker(iri);
			Model m;
			if (iccw.run()) {
				logger.trace("true");
				m = Utils.getTrue(iri);
			} else {
				logger.trace("false");
				m = Utils.getFalse(iri);
			}
			ByteArrayOutputStream bos = new ByteArrayOutputStream();
			m.write(bos, "RDF/XML");
			return Response.ok(bos.toString()).build();
		} catch (TestALODException e) {
			logger.trace("Error "+e.getMessage());
			e.printStackTrace();
		}
		return Response.serverError().build();
	}

}
