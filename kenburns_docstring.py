"""Ken Burns Slideshow Generation

This component of the INASRA application dynamically generates a slideshow using the Ken Burns effect,
a cinematic technique for adding motion to still images. Each slideshow is related to a specific word or concept,
enhancing the user experience through visual storytelling. The source images are dynamically provided through
an `images` array, populated by the server-side logic based on the current exploration context.

The selection process for these images involves:
1. Fetching relevant images from external sources like Wikipedia or Wikimedia Commons.
2. Filtering and selecting images based on relevance, quality, and metadata criteria.
3. Assigning the selected images to the `images` array, which is used in the `kenburns.html` Jinja template.
4. The template renders each image in the slideshow with an animation delay, creating the Ken Burns effect through CSS.

This process ensures that the Ken Burns slideshow offers visually engaging content corresponding to the users’ exploration,
fostering a deeper understanding and appreciation of the subject matter.
"""
