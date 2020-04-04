package it.cnr.istc.stlab.testalod.resources;

import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.ConsoleProgressMonitor;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.SimpleConfiguration;

public class Utils {

	private static final Logger logger = LogManager.getLogger(Utils.class);

	static boolean checkConsistency(String iriTestCase) throws OWLOntologyCreationException {

		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		OWLOntology ontology = manager.loadOntology(IRI.create(iriTestCase.toString()));

		ontology.importsClosure().forEach(ont -> {
			logger.trace("Importing " + ont.getOntologyID().getOntologyIRI().toString());
			ontology.addAxioms(ont.axioms());
		});

		OWLDataFactory factory = manager.getOWLDataFactory();

		ontology.annotations().forEach(a -> {
			if (a.containsEntityInSignature(factory.getOWLAnnotationProperty(
					"http://www.ontologydesignpatterns.org/schemas/testannotationschema.owl#hasInputTestData"))) {
				try {
					logger.trace("Importing " + a.getValue().toString());
					OWLOntology toyDataset = manager.loadOntology(IRI.create(a.getValue().toString()));
					toyDataset.importsClosure().forEach(ont -> {
						logger.trace("Importing " + ont.getOntologyID().getOntologyIRI().toString());
						ontology.addAxioms(ont.axioms());
					});
					ontology.addAxioms(toyDataset.axioms());
				} catch (OWLOntologyCreationException e) {
					e.printStackTrace();
				}
			}
		});

		ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
		OWLReasonerConfiguration config = new SimpleConfiguration(progressMonitor);
		OWLReasoner reasoner = new org.semanticweb.HermiT.ReasonerFactory().createReasoner(ontology, config);

		return reasoner.isConsistent();

	}
	
	
	static boolean checkIntegrityConstraint(String iriTestCase) throws OWLOntologyCreationException {

		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		OWLOntology ontology = manager.loadOntology(IRI.create(iriTestCase.toString()));

		ontology.importsClosure().forEach(ont -> {
			logger.trace("Importing " + ont.getOntologyID().getOntologyIRI().toString());
			ontology.addAxioms(ont.axioms());
		});

		OWLDataFactory factory = manager.getOWLDataFactory();

		ontology.annotations().forEach(a -> {
			if (a.containsEntityInSignature(factory.getOWLAnnotationProperty(
					"http://www.ontologydesignpatterns.org/schemas/testannotationschema.owl#hasInputTestData"))) {
				try {
					logger.trace("Importing " + a.getValue().toString());
					OWLOntology toyDataset = manager.loadOntology(IRI.create(a.getValue().toString()));
					toyDataset.importsClosure().forEach(ont -> {
						logger.trace("Importing " + ont.getOntologyID().getOntologyIRI().toString());
						ontology.addAxioms(ont.axioms());
					});
					ontology.addAxioms(toyDataset.axioms());
				} catch (OWLOntologyCreationException e) {
					e.printStackTrace();
				}
			}
		});

		ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
		OWLReasonerConfiguration config = new SimpleConfiguration(progressMonitor);
		OWLReasoner reasoner = new org.semanticweb.HermiT.ReasonerFactory().createReasoner(ontology, config);

		return reasoner.isConsistent();

	}

	public static void main(String[] args) throws OWLOntologyCreationException {
//		checkConsistency("file:///Users/lgu/Dropbox/repository/workspace/arco-git/ArCo-release/test/VI/testcase-01.owl");
		checkIntegrityConstraint(
				"https://raw.githubusercontent.com/ICCD-MiBACT/ArCo/master/ArCo-release/test/IC/testcase-01.owl");
	}

}
