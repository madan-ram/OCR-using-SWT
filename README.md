Stroke width transform
===================

This project objective describes an device dedicated for blind or   visually impaired people. The main aim of this system is to provide   an automated image classifier to classify the languages.   The challenge for such system is it should be a portable, low cost,   able to recognize distorted images, multiple languages and efficient   working in term of ability to recognize multiple size character. The   two key technologies are necessary: text detection and language   detection. A further improvement can also be done by integrating   it with Google translator which can be used by visually impaired   people .   Even though several researches have been done in this area ,it has   been observed that implementation of language detection is not yet   done. So a multi language detector is required for India, Since India   has several languages.

We implemented Stroke width transform a image operator that seeks to find the value of stroke width for each image pixel, and demonstrate its use on the task of text detection in natural images. The suggested operator is local and data dependent, which makes it fast and robust enough to eliminate the need for multi-scale computation or scanning windows. Extensive testing shows that the suggested scheme outperforms the latest published algorithms. Its simplicity allows the algorithm to detect texts in many fonts and languages. 

**List of algorithm implemented**
  * Stroke width transform (SWT) {For Text Detection}
  * Connected component labeling using DFS
  * Filtering component using Varinace or machine learning
  * Segmentation and language detection
  * Classification of chahracter
