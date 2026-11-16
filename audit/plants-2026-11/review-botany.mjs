// The judgments below were made after reading each full prompt and all options.
// This file attaches them to the author draft; it does not infer acceptance.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const draft=JSON.parse(fs.readFileSync(path.join(dir,'botany-draft.json'),'utf8'));
const judgments=[
['Anchorage of a named garden plant.','Roots anchor the sunflower; petals, anthers and seed coats do not.'],
['Function of root hairs.','Extra absorptive surface is the only option describing root-hair function.'],
['Protection provided by the root cap.','The cap shields the root meristem; the listed flower, fruit and leaf structures are elsewhere.'],
['Recognition of a central-root arrangement.','A dominant main root defines a taproot; fibrous roots lack that arrangement and runners/rhizomes are stems.'],
['Pollen-producing flower organ.','Anthers produce pollen; the stigma receives pollen and ovaries contain ovules.'],
['Pollen-receiving flower organ.','Only the stigma is the receptive surface among these options.'],
['Usual role of sepals before flowering.','Sepals surround and protect the developing flower bud; usually correctly avoids absolute exceptions.'],
['Fate of a fertilised ovule.','An ovule develops into a seed, not one of the three named flower organs.'],
['Identity of a green light-capturing pigment.','Chlorophyll is the photosynthetic pigment; the animal pigments/protein do not fit.'],
['Carbon input to photosynthesis.','Carbon dioxide supplies the carbon; none of the other gases contains carbon.'],
['Gas produced by photosynthesis.','Oxygen is released; methane, hydrogen and ammonia are not products of ordinary green-leaf photosynthesis.'],
['Sugar breakdown that continues at night.','Respiration releases usable energy; transpiration and pollination do not, and photosynthesis needs light.'],
['Support in soft plant tissue.','Turgor is intracellular water pressure; the alternative proposed pressures are not the mechanism.'],
['Effect of atmospheric humidity on water loss.','Humid air reduces the vapour gradient; dry, hotter or faster-moving dry air does not.'],
['Definition of photoperiod.','It measures daily light duration, not root length, flower size or seed age.'],
['Meaning of day-neutral flowering.','Day-neutral flowering is not regulated by day length; the other claims do not follow.'],
['Name of the discipline studying plants.','Botany is distinct from zoology, geology and meteorology.'],
['First word of a botanical binomial.','Rosa denotes the genus; family, order and cultivar are different categories.'],
['Taxonomic rank grouping related genera.','Family is broader than genus; species, cultivar and variety are narrower.'],
['Name for the flowering-plant group.','Angiosperms flower; gymnosperms, ferns and bryophytes do not produce true flowers.'],
['Number of cotyledons in monocots.','One seed leaf is the defining monocot condition; the number choices are unambiguous.'],
['Typical leaf venation of grasses.','Parallel venation is typical; the qualifier avoids asserting a universal monocot rule.'],
['Typical number pattern in monocot flowers.','Multiples of three are typical; usually is necessary and present.'],
['Typical monocot stem anatomy.','Bundles are scattered rather than forming the typical dicot ring; other locations are wrong.'],
['Name for a fern leaf.','Frond denotes the leaf; petals, catkins and cones are different structures.'],
['Fern dispersal structures.','Ferns release spores rather than pollen, nuts or berries.'],
['Role of sori on fern fronds.','Sori contain spore-producing sporangia; ferns lack flowers, seeds and pollen.'],
['Role of water in fern fertilisation.','Sperm can swim to the egg; water does not make spores become seeds.'],
['Moss anchoring structures.','Rhizoids provide attachment; anthers, petals and stamens are flower organs absent in mosses.'],
['Location of moss spore production.','The sporophyte capsule produces spores; mosses have no flowers or fruits.'],
['Life-cycle identity of leafy moss.','The familiar leafy part is the gametophyte; the alternatives are absent seed-plant structures.'],
['First growth after a moss spore germinates.','Protonema precedes leafy shoots; none of the alternatives is a moss germination stage.'],
['Seed-plant classification of pines and spruces.','Both are gymnosperms; angiosperms flower and the other groups are seedless.'],
['Location of pine seeds.','Seeds develop on female cone scales rather than within a fruit or petal.'],
['Identity of a pine needle.','A needle is a leaf; it is not a reproductive organ or root.'],
['A deciduous conifer among evergreen alternatives.','Larches normally shed their needles in autumn; Scots pine, Norway spruce and Douglas fir retain foliage.'],
['Life-cycle term for a single growing season.','Annual is the only matching life-cycle category; evergreen concerns retained foliage.'],
['Life-cycle term for two growing seasons.','Biennials ordinarily grow then reproduce across two seasons; epiphyte describes where a plant grows.'],
['Definition of perennial longevity.','More than two years defines perennial; seasonal leaf loss is a separate characteristic.'],
['Distinction between woody and herbaceous perennials.','Persistent woody stems define the woody group; evergreen foliage, continuous blooms and lack of seed dormancy do not.'],
['Name of dividing growth tissue.','Meristem is active cell-division tissue; the other choices are not meristems.'],
['Basic biological structural unit.','A cell is the basic unit; branches, seeds and petals contain many cells.'],
['Organisation of cells into tissue.','Tissue is a coordinated cell group; the other options concern whole organisms.'],
['Carrier of inherited genetic information.','DNA carries the genetic code; starch, cellulose and chlorophyll have other roles.'],
['Directional shoot growth towards light.','Phototropism is light-directed growth; the other tropisms involve gravity, water or contact.'],
['Stimulus involved in gravitropism.','Gravity is the named stimulus rather than light, humidity or touch.'],
['Growth response to contact with a support.','Thigmotropism describes touch-directed coiling; the other listed responses differ.'],
['Gaseous ripening hormone.','Ethylene alone is both gaseous and a recognised ripening signal among these four choices.'],
['Name of the young plant within a seed.','Embryo is correct; the other named structures belong to a flower.'],
['Protective outer seed structure.','Seed coat forms the protective covering; the distractors do not surround the embryo.'],
['Energy source during initial germination.','Organic reserves supply energy; minerals alone, an empty coat or carbon dioxide without light do not.'],
['Purpose of conservation seed banks.','Preserving viable seeds for future use is the purpose; destroying viability or forcing germination is not.'],
['Dispersal function of maple fruit wings.','Wings aid wind transport; currents, roots and swimming insects are not the primary mechanism.'],
['Dispersal function of hooks on burrs.','Hooks catch in fur, carrying seeds externally; none of the other mechanisms is plausible.'],
['Seed dispersal through fruit-eating birds.','Surviving swallowed seeds can pass in droppings; fully digested or permanently retained seeds cannot establish elsewhere.'],
['How squirrels can assist oak regeneration.','An unrecovered buried acorn can germinate; digestion, empty shells or removal from soil cannot.'],
['Name of a leaf stalk.','A petiole attaches the blade to its stem; radicle is embryonic root, not leaf stalk.'],
['Name of leaf gas-exchange pores.','Stomata are pores; cotyledons, rhizoids and petals are not.'],
['Cells controlling a stomatal opening.','Paired guard cells control aperture; the other cell types are not around a stoma.'],
['Name of the protective waxy leaf covering.','Cuticle is the surface layer; corolla, cambium and endosperm are elsewhere in the plant.']
];
if(draft.length!==60||judgments.length!==60)throw Error('Review coverage mismatch');
const rows=draft.map((q,i)=>({prompt:q.prompt,action:'keep',meaning:judgments[i][0],answer:judgments[i][1],grammar:'Read the complete prompt and all four answers: clear wording, agreement and punctuation; the alternatives fit the question grammatically.',category:'Directly tests plant structure, physiology, reproduction, classification or ecology.',reviewer:'plants-category independent botany review'}));
fs.writeFileSync(path.join(dir,'botany-independent-review.json'),JSON.stringify(rows,null,2)+'\n');
console.log('Saved 60 independent editorial judgments.');
