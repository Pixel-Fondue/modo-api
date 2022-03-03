#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""
.. module:: modo.constants
    :synopsis: Constants & defines used by the other modules in the package.

.. moduleauthor:: Gwynne Reddick <gwynne.reddick@thefoundry.co.uk>


"""

# from .mprop import mproperty
import lx

# Overriding the mprop.mproperty for bypassing pip install error with mproperty as a decorator.
def mproperty(*args):
    pass


SCENE_SVC = lx.service.Scene()
SEL_SVC = lx.service.Selection()
item_type = SCENE_SVC.ItemTypeLookup

# Commonly used item types - Constants implemented as module level properties for lazy lookup

@mproperty
def ABCDEFORM_SAMPLE_TYPE(constants):
    return item_type('ABCdeform.sample')

@mproperty
def ALEMBICCLOUD_TYPE(constants):
    return item_type('AlembicCloud')

@mproperty
def ALEMBICCURVES_TYPE(constants):
    return item_type('AlembicCurves')

@mproperty
def ALEMBICFILE_TYPE(constants):
    return item_type('AlembicFile')

@mproperty
def ALEMBICMESH_TYPE(constants):
    return item_type('AlembicMesh')

@mproperty
def EXPRESSION_TYPE(constants):
    return item_type('Expression')

@mproperty
def RPC_MESH_TYPE(constants):
    return item_type('RPC.Mesh')

@mproperty
def VOXELITEM_TYPE(constants):
    return item_type('VoxelItem')

@mproperty
def ACTIONCLIP_TYPE(constants):
    return item_type('actionclip')

@mproperty
def ACTIONPOSE_TYPE(constants):
    return item_type('actionpose')

@mproperty
def ADVANCEDMATERIAL_TYPE(constants):
    return item_type('advancedMaterial')

@mproperty
def ANCHOR_TYPE(constants):
    return item_type('anchor')

@mproperty
def AREALIGHT_TYPE(constants):
    return item_type('areaLight')

@mproperty
def AUDIOCLIP_TYPE(constants):
    return item_type('audioClip')

@mproperty
def AUDIOFILE_TYPE(constants):
    return item_type('audioFile')

@mproperty
def BACKDROP_TYPE(constants):
    return item_type('backdrop')

@mproperty
def BASEVOLUME_TYPE(constants):
    return item_type('baseVolume')

@mproperty
def BEZIERNODE_TYPE(constants):
    return item_type('bezierNode')

@mproperty
def BLOB_TYPE(constants):
    return item_type('blob')

@mproperty
def CAMERA_TYPE(constants):
    return item_type('camera')

@mproperty
def CAPSULE_TYPE(constants):
    return item_type('capsule')

@mproperty
def CEFLOAT_TYPE(constants):
    return item_type('ceFloat')

@mproperty
def CEMATRIX_TYPE(constants):
    return item_type('ceMatrix')

@mproperty
def CELLULAR_TYPE(constants):
    return item_type('cellular')

@mproperty
def CHANEFFECT_TYPE(constants):
    return item_type('chanEffect')

@mproperty
def CHANMODIFY_TYPE(constants):
    return item_type('chanModify')

@mproperty
def CHECKER_TYPE(constants):
    return item_type('checker')

@mproperty
def CMCHANNELRELATION_TYPE(constants):
    return item_type('cmChannelRelation')

@mproperty
def CMCLAMP_TYPE(constants):
    return item_type('cmClamp')

@mproperty
def CMCOLORBLEND_TYPE(constants):
    return item_type('cmColorBlend')

@mproperty
def CMCOLORCORRECT_TYPE(constants):
    return item_type('cmColorCorrect')

@mproperty
def CMCOLORGAMMA_TYPE(constants):
    return item_type('cmColorGamma')

@mproperty
def CMCOLORHSV_TYPE(constants):
    return item_type('cmColorHSV')

@mproperty
def CMCOLORINVERT_TYPE(constants):
    return item_type('cmColorInvert')

@mproperty
def CMCOLORKELVIN_TYPE(constants):
    return item_type('cmColorKelvin')

@mproperty
def CMCONSTANT_TYPE(constants):
    return item_type('cmConstant')

@mproperty
def CMCURVEPROBE_TYPE(constants):
    return item_type('cmCurveProbe')

@mproperty
def CMCYCLER_TYPE(constants):
    return item_type('cmCycler')

@mproperty
def CMDIRECTIONCONSTRAINT_TYPE(constants):
    return item_type('cmDirectionConstraint')

@mproperty
def CMDISTANCECONSTRAINT_TYPE(constants):
    return item_type('cmDistanceConstraint')

@mproperty
def CMDYNAMICPARENT_TYPE(constants):
    return item_type('cmDynamicParent')

@mproperty
def CMFLOATOFFSET_TYPE(constants):
    return item_type('cmFloatOffset')

@mproperty
def CMFLOATWARP_TYPE(constants):
    return item_type('cmFloatWarp')

@mproperty
def CMGEOMETRYCONSTRAINT_TYPE(constants):
    return item_type('cmGeometryConstraint')

@mproperty
def CMIKDUAL2D_TYPE(constants):
    return item_type('cmIKDual2D')

@mproperty
def CMINTERSECT_TYPE(constants):
    return item_type('cmIntersect')

@mproperty
def CMLINEARBLEND_TYPE(constants):
    return item_type('cmLinearBlend')

@mproperty
def CMLOGIC_TYPE(constants):
    return item_type('cmLogic')

@mproperty
def CMMATH_TYPE(constants):
    return item_type('cmMath')

@mproperty
def CMMATHBASIC_TYPE(constants):
    return item_type('cmMathBasic')

@mproperty
def CMMATHMULTI_TYPE(constants):
    return item_type('cmMathMulti')

@mproperty
def CMMATHTRIG_TYPE(constants):
    return item_type('cmMathTrig')

@mproperty
def CMMATHVECTOR_TYPE(constants):
    return item_type('cmMathVector')

@mproperty
def CMMATRIXBLEND_TYPE(constants):
    return item_type('cmMatrixBlend')

@mproperty
def CMMATRIXCOMPOSE_TYPE(constants):
    return item_type('cmMatrixCompose')

@mproperty
def CMMATRIXCONSTRUCT_TYPE(constants):
    return item_type('cmMatrixConstruct')

@mproperty
def CMMATRIXFROMEULER_TYPE(constants):
    return item_type('cmMatrixFromEuler')

@mproperty
def CMMATRIXINVERT_TYPE(constants):
    return item_type('cmMatrixInvert')

@mproperty
def CMMATRIXOFFSET_TYPE(constants):
    return item_type('cmMatrixOffset')

@mproperty
def CMMATRIXTOEULER_TYPE(constants):
    return item_type('cmMatrixToEuler')

@mproperty
def CMMATRIXTRANSPOSE_TYPE(constants):
    return item_type('cmMatrixTranspose')

@mproperty
def CMMATRIXVECTOR_TYPE(constants):
    return item_type('cmMatrixVector')

@mproperty
def CMMATRIXVECTORMULTIPLY_TYPE(constants):
    return item_type('cmMatrixVectorMultiply')

@mproperty
def CMMATRIXWARP_TYPE(constants):
    return item_type('cmMatrixWarp')

@mproperty
def CMMEASUREANGLE_TYPE(constants):
    return item_type('cmMeasureAngle')

@mproperty
def CMMEASUREDISTANCE_TYPE(constants):
    return item_type('cmMeasureDistance')

@mproperty
def CMNOISE_TYPE(constants):
    return item_type('cmNoise')

@mproperty
def CMOSCILLATOR_TYPE(constants):
    return item_type('cmOscillator')

@mproperty
def CMPID_TYPE(constants):
    return item_type('cmPID')

@mproperty
def CMPATHCONSTRAINT_TYPE(constants):
    return item_type('cmPathConstraint')

@mproperty
def CMQUATERNIONCONJUGATE_TYPE(constants):
    return item_type('cmQuaternionConjugate')

@mproperty
def CMQUATERNIONFROMAXISANGLE_TYPE(constants):
    return item_type('cmQuaternionFromAxisAngle')

@mproperty
def CMQUATERNIONFROMEULER_TYPE(constants):
    return item_type('cmQuaternionFromEuler')

@mproperty
def CMQUATERNIONFROMMATRIX_TYPE(constants):
    return item_type('cmQuaternionFromMatrix')

@mproperty
def CMQUATERNIONGETVALUE_TYPE(constants):
    return item_type('cmQuaternionGetValue')

@mproperty
def CMQUATERNIONMATH_TYPE(constants):
    return item_type('cmQuaternionMath')

@mproperty
def CMQUATERNIONNORMALIZE_TYPE(constants):
    return item_type('cmQuaternionNormalize')

@mproperty
def CMQUATERNIONSETVALUE_TYPE(constants):
    return item_type('cmQuaternionSetValue')

@mproperty
def CMQUATERNIONSLERP_TYPE(constants):
    return item_type('cmQuaternionSlerp')

@mproperty
def CMQUATERNIONTOAXISANGLE_TYPE(constants):
    return item_type('cmQuaternionToAxisAngle')

@mproperty
def CMQUATERNIONTOEULER_TYPE(constants):
    return item_type('cmQuaternionToEuler')

@mproperty
def CMQUATERNIONTOMATRIX_TYPE(constants):
    return item_type('cmQuaternionToMatrix')

@mproperty
def CMQUATERNIONVECTORMULTIPLY_TYPE(constants):
    return item_type('cmQuaternionVectorMultiply')

@mproperty
def CMRANDOM_TYPE(constants):
    return item_type('cmRandom')

@mproperty
def CMREVOLVE_TYPE(constants):
    return item_type('cmRevolve')

@mproperty
def CMSHADEREFFECTS_TYPE(constants):
    return item_type('cmShaderEffects')

@mproperty
def CMSHADERLIGHTING_TYPE(constants):
    return item_type('cmShaderLighting')

@mproperty
def CMSHADERRAYTYPE_TYPE(constants):
    return item_type('cmShaderRayType')

@mproperty
def CMSHADERRAYCAST_TYPE(constants):
    return item_type('cmShaderRaycast')

@mproperty
def CMSHADERSWITCH_TYPE(constants):
    return item_type('cmShaderSwitch')

@mproperty
def CMSIMPLEKINEMATICS_TYPE(constants):
    return item_type('cmSimpleKinematics')

@mproperty
def CMSMOOTH_TYPE(constants):
    return item_type('cmSmooth')

@mproperty
def CMSOUND_TYPE(constants):
    return item_type('cmSound')

@mproperty
def CMSPEED_TYPE(constants):
    return item_type('cmSpeed')

@mproperty
def CMSTRINGCOMPOSE_TYPE(constants):
    return item_type('cmStringCompose')

@mproperty
def CMSTRINGFINDANDREPLACE_TYPE(constants):
    return item_type('cmStringFindAndReplace')

@mproperty
def CMSTRINGSWITCH_TYPE(constants):
    return item_type('cmStringSwitch')

@mproperty
def CMSWITCH_TYPE(constants):
    return item_type('cmSwitch')

@mproperty
def CMTIME_TYPE(constants):
    return item_type('cmTime')

@mproperty
def CMTRANSFORMCONSTRAINT_TYPE(constants):
    return item_type('cmTransformConstraint')

@mproperty
def CMVECTOR_TYPE(constants):
    return item_type('cmVector')

@mproperty
def CMVECTORBYSCALAR_TYPE(constants):
    return item_type('cmVectorByScalar')

@mproperty
def CMVECTORMAGNITUDE_TYPE(constants):
    return item_type('cmVectorMagnitude')

@mproperty
def CMVECTORORTHOGONALIZE_TYPE(constants):
    return item_type('cmVectorOrthogonalize')

@mproperty
def CMVECTORREFLECTION_TYPE(constants):
    return item_type('cmVectorReflection')

@mproperty
def CMVELOCITY_TYPE(constants):
    return item_type('cmVelocity')

@mproperty
def CMWAVEFORM_TYPE(constants):
    return item_type('cmWaveform')

@mproperty
def COLLECTOREMITTER_TYPE(constants):
    return item_type('collectorEmitter')

@mproperty
def CONS_TYPE(constants):
    return item_type('cons')

@mproperty
def CONSHINGE_TYPE(constants):
    return item_type('consHinge')

@mproperty
def CONSPIN_TYPE(constants):
    return item_type('consPin')

@mproperty
def CONSPOINT_TYPE(constants):
    return item_type('consPoint')

@mproperty
def CONSSLIDEHINGE_TYPE(constants):
    return item_type('consSlideHinge')

@mproperty
def CONSSPRING_TYPE(constants):
    return item_type('consSpring')

@mproperty
def CONSTANT_TYPE(constants):
    return item_type('constant')

@mproperty
def CSVCACHE_TYPE(constants):
    return item_type('csvCache')

@mproperty
def CURVEEMITTER_TYPE(constants):
    return item_type('curveEmitter')

@mproperty
def CYLINDERLIGHT_TYPE(constants):
    return item_type('cylinderLight')

@mproperty
def DEFAULTSHADER_TYPE(constants):
    return item_type('defaultShader')

@mproperty
def DEFERREDMESH_TYPE(constants):
    return item_type('deferredMesh')

@mproperty
def DEFORM_TYPE(constants):
    return item_type('deform')

@mproperty
def DEFORM_BEND_TYPE(constants):
    return item_type('deform.bend')

@mproperty
def DEFORM_BEZIER_TYPE(constants):
    return item_type('deform.bezier')

@mproperty
def DEFORM_CRVCONST_TYPE(constants):
    return item_type('deform.crvConst')

@mproperty
def DEFORM_LAG_TYPE(constants):
    return item_type('deform.lag')

@mproperty
def DEFORM_LATTICE_TYPE(constants):
    return item_type('deform.lattice')

@mproperty
def DEFORM_MAGNET_TYPE(constants):
    return item_type('deform.magnet')

@mproperty
def DEFORM_SLACK_TYPE(constants):
    return item_type('deform.slack')

@mproperty
def DEFORM_SPLINE_TYPE(constants):
    return item_type('deform.spline')

@mproperty
def DEFORM_VORTEX_TYPE(constants):
    return item_type('deform.vortex')

@mproperty
def DEFORM_WRAP_TYPE(constants):
    return item_type('deform.wrap')

@mproperty
def DEFORMFOLDER_TYPE(constants):
    return item_type('deformFolder')

@mproperty
def DEFORMGROUP_TYPE(constants):
    return item_type('deformGroup')

@mproperty
def DEFORMMDD_TYPE(constants):
    return item_type('deformMDD')

@mproperty
def DEFORMMDD2_TYPE(constants):
    return item_type('deformMDD2')

@mproperty
def DOMELIGHT_TYPE(constants):
    return item_type('domeLight')

@mproperty
def DOTS_TYPE(constants):
    return item_type('dots')

@mproperty
def DYNAMIC_REPLICATORFILTER_TYPE(constants):
    return item_type('dynamic.replicatorFilter')

@mproperty
def DYNAMICCOLLIDER_TYPE(constants):
    return item_type('dynamicCollider')

@mproperty
def DYNAMICCOLLISIONEMITTER_TYPE(constants):
    return item_type('dynamicCollisionEmitter')

@mproperty
def DYNAMICFLUID_TYPE(constants):
    return item_type('dynamicFluid')

@mproperty
def DYNAMICSCONSTRAINTMODIFIER_TYPE(constants):
    return item_type('dynamicsConstraintModifier')

@mproperty
def ENVMATERIAL_TYPE(constants):
    return item_type('envMaterial')

@mproperty
def ENVIRONMENT_TYPE(constants):
    return item_type('environment')

@mproperty
def FALLOFF_TYPE(constants):
    return item_type('falloff')

@mproperty
def FALLOFF_BEZIER_TYPE(constants):
    return item_type('falloff.bezier')

@mproperty
def FALLOFF_CAPSULE_TYPE(constants):
    return item_type('falloff.capsule')

@mproperty
def FALLOFF_LINEAR_TYPE(constants):
    return item_type('falloff.linear')

@mproperty
def FALLOFF_RADIAL_TYPE(constants):
    return item_type('falloff.radial')

@mproperty
def FALLOFF_SPLINE_TYPE(constants):
    return item_type('falloff.spline')

@mproperty
def FLOCKINGOP_TYPE(constants):
    return item_type('flockingOp')

@mproperty
def FORCE_CURVE_TYPE(constants):
    return item_type('force.curve')

@mproperty
def FORCE_DRAG_TYPE(constants):
    return item_type('force.drag')

@mproperty
def FORCE_LINEAR_TYPE(constants):
    return item_type('force.linear')

@mproperty
def FORCE_NEWTON_TYPE(constants):
    return item_type('force.newton')

@mproperty
def FORCE_RADIAL_TYPE(constants):
    return item_type('force.radial')

@mproperty
def FORCE_ROOT_TYPE(constants):
    return item_type('force.root')

@mproperty
def FORCE_TURBULENCE_TYPE(constants):
    return item_type('force.turbulence')

@mproperty
def FORCE_VORTEX_TYPE(constants):
    return item_type('force.vortex')

@mproperty
def FORCE_WIND_TYPE(constants):
    return item_type('force.wind')

@mproperty
def FURMATERIAL_TYPE(constants):
    return item_type('furMaterial')

@mproperty
def GASKETTOY_TYPE(constants):
    return item_type('gaskettoy')

@mproperty
def GEAR_ITEM_TYPE(constants):
    return item_type('gear.item')

@mproperty
def GENINFLUENCE_TYPE(constants):
    return item_type('genInfluence')

@mproperty
def GPLANE_TYPE(constants):
    return item_type('gplane')

@mproperty
def GRADIENT_TYPE(constants):
    return item_type('gradient')

@mproperty
def GRASS_ITEM_TYPE(constants):
    return item_type('grass.item')

@mproperty
def GRID_TYPE(constants):
    return item_type('grid')

@mproperty
def GROUP_TYPE(constants):
    return item_type('group')

@mproperty
def GROUPLOCATOR_TYPE(constants):
    return item_type('groupLocator')

@mproperty
def IKFULLBODY_TYPE(constants):
    return item_type('ikFullBody')

@mproperty
def IKSOLVER_TYPE(constants):
    return item_type('ikSolver')

@mproperty
def IMAGEFOLDER_TYPE(constants):
    return item_type('imageFolder')

@mproperty
def IMAGEGROUP_TYPE(constants):
    return item_type('imageGroup')

@mproperty
def IMAGELAYER_TYPE(constants):
    return item_type('imageLayer')

@mproperty
def IMAGEMAP_TYPE(constants):
    return item_type('imageMap')

@mproperty
def ITEM_ROCK_TYPE(constants):
    return item_type('item.rock')

@mproperty
def ITEMCHANNELPROBE_TYPE(constants):
    return item_type('itemChannelProbe')

@mproperty
def ITEMINFLUENCE_TYPE(constants):
    return item_type('itemInfluence')

@mproperty
def ITEMMODIFY_TYPE(constants):
    return item_type('itemModify')

@mproperty
def LIGHT_TYPE(constants):
    return item_type('light')

@mproperty
def LIGHTMATERIAL_TYPE(constants):
    return item_type('lightMaterial')

@mproperty
def LOCATOR_TYPE(constants):
    return item_type('locator')

@mproperty
def LOCDEFORM_TYPE(constants):
    return item_type('locdeform')

@mproperty
def MAPMIX_TYPE(constants):
    return item_type('mapMix')

@mproperty
def MASK_TYPE(constants):
    return item_type('mask')

@mproperty
def MATCAPSHADER_TYPE(constants):
    return item_type('matcapShader')

@mproperty
def MATERIAL_CELEDGES_TYPE(constants):
    return item_type('material.celEdges')

@mproperty
def MATERIAL_CELSHADER_TYPE(constants):
    return item_type('material.celShader')

@mproperty
def MATERIAL_HAIRMATERIAL_TYPE(constants):
    return item_type('material.hairMaterial')

@mproperty
def MATERIAL_HALFTONE_TYPE(constants):
    return item_type('material.halftone')

@mproperty
def MATERIAL_IRIDESCENCE_TYPE(constants):
    return item_type('material.iridescence')

@mproperty
def MATERIAL_SKINMATERIAL_TYPE(constants):
    return item_type('material.skinMaterial')

@mproperty
def MATERIAL_THINFILM_TYPE(constants):
    return item_type('material.thinfilm')

@mproperty
def MEDIACLIP_TYPE(constants):
    return item_type('mediaClip')

@mproperty
def MESH_TYPE(constants):
    return item_type('mesh')

@mproperty
def MESHINST_TYPE(constants):
    return item_type('meshInst')

@mproperty
def MORPHDEFORM_TYPE(constants):
    return item_type('morphDeform')

@mproperty
def MORPHMIX_TYPE(constants):
    return item_type('morphMix')

@mproperty
def NOISE_TYPE(constants):
    return item_type('noise')

@mproperty
def OCCLUSION_TYPE(constants):
    return item_type('occlusion')

@mproperty
def PMOD_AUDIO_TYPE(constants):
    return item_type('pMod.audio')

@mproperty
def PMOD_BASIC_TYPE(constants):
    return item_type('pMod.basic')

@mproperty
def PMOD_EXPRESSION_TYPE(constants):
    return item_type('pMod.expression')

@mproperty
def PMOD_GENERATOR_TYPE(constants):
    return item_type('pMod.generator')

@mproperty
def PMOD_LOOKAT_TYPE(constants):
    return item_type('pMod.lookat')

@mproperty
def PMOD_RANDOM_TYPE(constants):
    return item_type('pMod.random')

@mproperty
def PMOD_SIEVE_TYPE(constants):
    return item_type('pMod.sieve')

@mproperty
def PMOD_STEP_TYPE(constants):
    return item_type('pMod.step')

@mproperty
def PARTICLEOP_TYPE(constants):
    return item_type('particleOp')

@mproperty
def PARTICLESIM_TYPE(constants):
    return item_type('particleSim')

@mproperty
def PARTICLETERMINATOR_TYPE(constants):
    return item_type('particleTerminator')

@mproperty
def PCLOUD_TYPE(constants):
    return item_type('pcloud')

@mproperty
def PHOTOMETRYLIGHT_TYPE(constants):
    return item_type('photometryLight')

@mproperty
def POINTLIGHT_TYPE(constants):
    return item_type('pointLight')

@mproperty
def POLYRENDER_TYPE(constants):
    return item_type('polyRender')

@mproperty
def PORTAL_TYPE(constants):
    return item_type('portal')

@mproperty
def PROBEFALLOFF_TYPE(constants):
    return item_type('probeFalloff')

@mproperty
def PROCESS_TYPE(constants):
    return item_type('process')

@mproperty
def PROJECTSHADER_TYPE(constants):
    return item_type('projectShader')

@mproperty
def PROXY_TYPE(constants):
    return item_type('proxy')

@mproperty
def RADIALEMITTER_TYPE(constants):
    return item_type('radialEmitter')

@mproperty
def REALPARTICLE_TYPE(constants):
    return item_type('realParticle')

@mproperty
def RENDER_TYPE(constants):
    return item_type('render')

@mproperty
def RENDERBOOL_TYPE(constants):
    return item_type('renderBool')

@mproperty
def RENDEROUTPUT_TYPE(constants):
    return item_type('renderOutput')

@mproperty
def REPLICATOR_TYPE(constants):
    return item_type('replicator')

@mproperty
def RIPPLES_TYPE(constants):
    return item_type('ripples')

@mproperty
def ROTATION_TYPE(constants):
    return item_type('rotation')

@mproperty
def SCALE_TYPE(constants):
    return item_type('scale')

@mproperty
def SCENE_TYPE(constants):
    return item_type('scene')

@mproperty
def SCHMNODE_TYPE(constants):
    return item_type('schmNode')

@mproperty
def SHADER_TYPE(constants):
    return item_type('shader')

@mproperty
def SHADERFOLDER_TYPE(constants):
    return item_type('shaderFolder')

@mproperty
def SHEAR_TYPE(constants):
    return item_type('shear')

@mproperty
def SOFTLAG_TYPE(constants):
    return item_type('softLag')

@mproperty
def SOLVER_TYPE(constants):
    return item_type('solver')

@mproperty
def SOURCEEMITTER_TYPE(constants):
    return item_type('sourceEmitter')

@mproperty
def SPOTLIGHT_TYPE(constants):
    return item_type('spotLight')

@mproperty
def SPRITE_TYPE(constants):
    return item_type('sprite')

@mproperty
def SUNLIGHT_TYPE(constants):
    return item_type('sunLight')

@mproperty
def SURFEMITTER_TYPE(constants):
    return item_type('surfEmitter')

@mproperty
def SURFGEN_TYPE(constants):
    return item_type('surfGen')

@mproperty
def SURFGENLOC_TYPE(constants):
    return item_type('surfGenLoc')

@mproperty
def SURFACESCATTER_TYPE(constants):
    return item_type('surfaceScatter')

@mproperty
def TENSIONTEXTURE_TYPE(constants):
    return item_type('tensionTexture')

@mproperty
def TEXTURELAYER_TYPE(constants):
    return item_type('textureLayer')

@mproperty
def TRANSFORM_TYPE(constants):
    return item_type('transform')

@mproperty
def TRANSLATION_TYPE(constants):
    return item_type('translation')

@mproperty
def TRISURF_TYPE(constants):
    return item_type('triSurf')

@mproperty
def TXTRLOCATOR_TYPE(constants):
    return item_type('txtrLocator')

@mproperty
def VAL_DISPLAY_COUNTER1_RJJ_TYPE(constants):
    return item_type('val.Display_Counter1.RJJ')

@mproperty
def VAL_DISPLAY_COUNTER2_RJJ_TYPE(constants):
    return item_type('val.Display_Counter2.RJJ')

@mproperty
def VAL_DISPLAY_UVLEDS_RJJ_TYPE(constants):
    return item_type('val.Display_UVLEDs.RJJ')

@mproperty
def VAL_GEOMETRIC_BOX_RJJ_TYPE(constants):
    return item_type('val.Geometric_Box.RJJ')

@mproperty
def VAL_GEOMETRIC_CIRCULAR_RJJ_TYPE(constants):
    return item_type('val.Geometric_Circular.RJJ')

@mproperty
def VAL_GEOMETRIC_CORNERS_RJJ_TYPE(constants):
    return item_type('val.Geometric_Corners.RJJ')

@mproperty
def VAL_GEOMETRIC_CUBIC_RJJ_TYPE(constants):
    return item_type('val.Geometric_Cubic.RJJ')

@mproperty
def VAL_GEOMETRIC_DIMPLES_RJJ_TYPE(constants):
    return item_type('val.Geometric_Dimples.RJJ')

@mproperty
def VAL_GEOMETRIC_GRID_RJJ_TYPE(constants):
    return item_type('val.Geometric_Grid.RJJ')

@mproperty
def VAL_GEOMETRIC_IRIS_RJJ_TYPE(constants):
    return item_type('val.Geometric_Iris.RJJ')

@mproperty
def VAL_GEOMETRIC_LINEAR_RJJ_TYPE(constants):
    return item_type('val.Geometric_Linear.RJJ')

@mproperty
def VAL_GEOMETRIC_POLYGON_RJJ_TYPE(constants):
    return item_type('val.Geometric_Polygon.RJJ')

@mproperty
def VAL_GEOMETRIC_RADIAL_RJJ_TYPE(constants):
    return item_type('val.Geometric_Radial.RJJ')

@mproperty
def VAL_GEOMETRIC_RING_RJJ_TYPE(constants):
    return item_type('val.Geometric_Ring.RJJ')

@mproperty
def VAL_GEOMETRIC_RNDLINEAR_RJJ_TYPE(constants):
    return item_type('val.Geometric_RndLinear.RJJ')

@mproperty
def VAL_GEOMETRIC_SPIRAL_RJJ_TYPE(constants):
    return item_type('val.Geometric_Spiral.RJJ')

@mproperty
def VAL_GEOMETRIC_STAR_RJJ_TYPE(constants):
    return item_type('val.Geometric_Star.RJJ')

@mproperty
def VAL_NOISE_AGATE_RJJ_TYPE(constants):
    return item_type('val.Noise_Agate.RJJ')

@mproperty
def VAL_NOISE_BOZO_RJJ_TYPE(constants):
    return item_type('val.Noise_Bozo.RJJ')

@mproperty
def VAL_NOISE_CRUDDY_RJJ_TYPE(constants):
    return item_type('val.Noise_Cruddy.RJJ')

@mproperty
def VAL_NOISE_DENTED_RJJ_TYPE(constants):
    return item_type('val.Noise_Dented.RJJ')

@mproperty
def VAL_NOISE_ETCHED_RJJ_TYPE(constants):
    return item_type('val.Noise_Etched.RJJ')

@mproperty
def VAL_NOISE_FLOWBOZO_RJJ_TYPE(constants):
    return item_type('val.Noise_FlowBozo.RJJ')

@mproperty
def VAL_NOISE_GRANITE_RJJ_TYPE(constants):
    return item_type('val.Noise_Granite.RJJ')

@mproperty
def VAL_NOISE_HYBRID_RJJ_TYPE(constants):
    return item_type('val.Noise_Hybrid.RJJ')

@mproperty
def VAL_NOISE_LUMP_RJJ_TYPE(constants):
    return item_type('val.Noise_Lump.RJJ')

@mproperty
def VAL_NOISE_MARBLENOISE_RJJ_TYPE(constants):
    return item_type('val.Noise_MarbleNoise.RJJ')

@mproperty
def VAL_NOISE_MARBLEVEIN_RJJ_TYPE(constants):
    return item_type('val.Noise_MarbleVein.RJJ')

@mproperty
def VAL_NOISE_MULTIFRACTAL_RJJ_TYPE(constants):
    return item_type('val.Noise_MultiFractal.RJJ')

@mproperty
def VAL_NOISE_PEBBLES_RJJ_TYPE(constants):
    return item_type('val.Noise_Pebbles.RJJ')

@mproperty
def VAL_NOISE_PUFFYCLOUDS_RJJ_TYPE(constants):
    return item_type('val.Noise_PuffyClouds.RJJ')

@mproperty
def VAL_NOISE_RIDGED_RJJ_TYPE(constants):
    return item_type('val.Noise_Ridged.RJJ')

@mproperty
def VAL_NOISE_SCAR_RJJ_TYPE(constants):
    return item_type('val.Noise_Scar.RJJ')

@mproperty
def VAL_NOISE_SCRUFFED_RJJ_TYPE(constants):
    return item_type('val.Noise_Scruffed.RJJ')

@mproperty
def VAL_NOISE_STRATA_RJJ_TYPE(constants):
    return item_type('val.Noise_Strata.RJJ')

@mproperty
def VAL_NOISE_STUCCO_RJJ_TYPE(constants):
    return item_type('val.Noise_Stucco.RJJ')

@mproperty
def VAL_NOISE_VECTORBOZO_RJJ_TYPE(constants):
    return item_type('val.Noise_VectorBozo.RJJ')

@mproperty
def VAL_NOISE_WRAPPEDFBM_RJJ_TYPE(constants):
    return item_type('val.Noise_WrappedfBm.RJJ')

@mproperty
def VAL_NOISE_FBM_RJJ_TYPE(constants):
    return item_type('val.Noise_fBm.RJJ')

@mproperty
def VAL_ORGANIC_ARTDECO_RJJ_TYPE(constants):
    return item_type('val.Organic_ArtDeco.RJJ')

@mproperty
def VAL_ORGANIC_BLISTER_RJJ_TYPE(constants):
    return item_type('val.Organic_Blister.RJJ')

@mproperty
def VAL_ORGANIC_BRANCHES_RJJ_TYPE(constants):
    return item_type('val.Organic_Branches.RJJ')

@mproperty
def VAL_ORGANIC_CAUSTIC_RJJ_TYPE(constants):
    return item_type('val.Organic_Caustic.RJJ')

@mproperty
def VAL_ORGANIC_CELLULAR_RJJ_TYPE(constants):
    return item_type('val.Organic_Cellular.RJJ')

@mproperty
def VAL_ORGANIC_CHEESY_RJJ_TYPE(constants):
    return item_type('val.Organic_Cheesy.RJJ')

@mproperty
def VAL_ORGANIC_CONCRETE_RJJ_TYPE(constants):
    return item_type('val.Organic_Concrete.RJJ')

@mproperty
def VAL_ORGANIC_CRACKLE_RJJ_TYPE(constants):
    return item_type('val.Organic_Crackle.RJJ')

@mproperty
def VAL_ORGANIC_DIRT_RJJ_TYPE(constants):
    return item_type('val.Organic_Dirt.RJJ')

@mproperty
def VAL_ORGANIC_DISTURBED_RJJ_TYPE(constants):
    return item_type('val.Organic_Disturbed.RJJ')

@mproperty
def VAL_ORGANIC_EASYWOOD_RJJ_TYPE(constants):
    return item_type('val.Organic_EasyWood.RJJ')

@mproperty
def VAL_ORGANIC_ELECTRIC_RJJ_TYPE(constants):
    return item_type('val.Organic_Electric.RJJ')

@mproperty
def VAL_ORGANIC_FIRE_RJJ_TYPE(constants):
    return item_type('val.Organic_Fire.RJJ')

@mproperty
def VAL_ORGANIC_FIREWALL_RJJ_TYPE(constants):
    return item_type('val.Organic_FireWall.RJJ')

@mproperty
def VAL_ORGANIC_HARDWOOD_RJJ_TYPE(constants):
    return item_type('val.Organic_HardWood.RJJ')

@mproperty
def VAL_ORGANIC_MEMBRANE_RJJ_TYPE(constants):
    return item_type('val.Organic_Membrane.RJJ')

@mproperty
def VAL_ORGANIC_MINKY_RJJ_TYPE(constants):
    return item_type('val.Organic_Minky.RJJ')

@mproperty
def VAL_ORGANIC_SCATTER_RJJ_TYPE(constants):
    return item_type('val.Organic_Scatter.RJJ')

@mproperty
def VAL_ORGANIC_SINBLOB_RJJ_TYPE(constants):
    return item_type('val.Organic_SinBlob.RJJ')

@mproperty
def VAL_ORGANIC_VEINS_RJJ_TYPE(constants):
    return item_type('val.Organic_Veins.RJJ')

@mproperty
def VAL_ORGANIC_WIRES_RJJ_TYPE(constants):
    return item_type('val.Organic_Wires.RJJ')

@mproperty
def VAL_ORGANIC_WORMVEIN_RJJ_TYPE(constants):
    return item_type('val.Organic_WormVein.RJJ')

@mproperty
def VAL_PANELS_PEEL_RJJ_TYPE(constants):
    return item_type('val.Panels_Peel.RJJ')

@mproperty
def VAL_PANELS_PLATES_RJJ_TYPE(constants):
    return item_type('val.Panels_Plates.RJJ')

@mproperty
def VAL_PANELS_RIVETRUST_RJJ_TYPE(constants):
    return item_type('val.Panels_RivetRust.RJJ')

@mproperty
def VAL_PANELS_RIVETS_RJJ_TYPE(constants):
    return item_type('val.Panels_Rivets.RJJ')

@mproperty
def VAL_PANELS_RUST_RJJ_TYPE(constants):
    return item_type('val.Panels_Rust.RJJ')

@mproperty
def VAL_PANELS_SMEAR_RJJ_TYPE(constants):
    return item_type('val.Panels_Smear.RJJ')

@mproperty
def VAL_PROCESS_EASYGRAD_RJJ_TYPE(constants):
    return item_type('val.Process_EasyGrad.RJJ')

@mproperty
def VAL_PROCESS_REGIONALHSV_RJJ_TYPE(constants):
    return item_type('val.Process_RegionalHSV.RJJ')

@mproperty
def VAL_RTCURVATURE_TYPE(constants):
    return item_type('val.RTCurvature')

@mproperty
def VAL_RPCTEXTURE_TYPE(constants):
    return item_type('val.RpcTexture')

@mproperty
def VAL_SKINS_CAMO_RJJ_TYPE(constants):
    return item_type('val.Skins_Camo.RJJ')

@mproperty
def VAL_SKINS_CRUMPLED_RJJ_TYPE(constants):
    return item_type('val.Skins_Crumpled.RJJ')

@mproperty
def VAL_SKINS_DINOSKIN_RJJ_TYPE(constants):
    return item_type('val.Skins_DinoSkin.RJJ')

@mproperty
def VAL_SKINS_DISEASE_RJJ_TYPE(constants):
    return item_type('val.Skins_Disease.RJJ')

@mproperty
def VAL_SKINS_FROGSKIN_RJJ_TYPE(constants):
    return item_type('val.Skins_FrogSkin.RJJ')

@mproperty
def VAL_SKINS_GRAINYWOOD_RJJ_TYPE(constants):
    return item_type('val.Skins_GrainyWood.RJJ')

@mproperty
def VAL_SKINS_LEATHER_RJJ_TYPE(constants):
    return item_type('val.Skins_Leather.RJJ')

@mproperty
def VAL_SKINS_MONSTER_RJJ_TYPE(constants):
    return item_type('val.Skins_Monster.RJJ')

@mproperty
def VAL_SKINS_PASTELLA_RJJ_TYPE(constants):
    return item_type('val.Skins_Pastella.RJJ')

@mproperty
def VAL_SKINS_PEENED_RJJ_TYPE(constants):
    return item_type('val.Skins_Peened.RJJ')

@mproperty
def VAL_SKINS_SCRATCHES_RJJ_TYPE(constants):
    return item_type('val.Skins_Scratches.RJJ')

@mproperty
def VAL_SPACE_BLAST_RJJ_TYPE(constants):
    return item_type('val.Space_Blast.RJJ')

@mproperty
def VAL_SPACE_CORIOLIS_RJJ_TYPE(constants):
    return item_type('val.Space_Coriolis.RJJ')

@mproperty
def VAL_SPACE_FLARE_RJJ_TYPE(constants):
    return item_type('val.Space_Flare.RJJ')

@mproperty
def VAL_SPACE_GASGIANT_RJJ_TYPE(constants):
    return item_type('val.Space_GasGiant.RJJ')

@mproperty
def VAL_SPACE_GLINT_RJJ_TYPE(constants):
    return item_type('val.Space_Glint.RJJ')

@mproperty
def VAL_SPACE_HURRICANE_RJJ_TYPE(constants):
    return item_type('val.Space_Hurricane.RJJ')

@mproperty
def VAL_SPACE_NURNIES_RJJ_TYPE(constants):
    return item_type('val.Space_Nurnies.RJJ')

@mproperty
def VAL_SPACE_PLANET_RJJ_TYPE(constants):
    return item_type('val.Space_Planet.RJJ')

@mproperty
def VAL_SPACE_PLANETCLOUDS_RJJ_TYPE(constants):
    return item_type('val.Space_PlanetClouds.RJJ')

@mproperty
def VAL_SPACE_RINGS_RJJ_TYPE(constants):
    return item_type('val.Space_Rings.RJJ')

@mproperty
def VAL_SPACE_STARFIELD_RJJ_TYPE(constants):
    return item_type('val.Space_StarField.RJJ')

@mproperty
def VAL_SPACE_SWIRL_RJJ_TYPE(constants):
    return item_type('val.Space_Swirl.RJJ')

@mproperty
def VAL_SPACE_TERRA_RJJ_TYPE(constants):
    return item_type('val.Space_Terra.RJJ')

@mproperty
def VAL_SPACE_WINDOWS_RJJ_TYPE(constants):
    return item_type('val.Space_Windows.RJJ')

@mproperty
def VAL_TILES_BASKET_RJJ_TYPE(constants):
    return item_type('val.Tiles_Basket.RJJ')

@mproperty
def VAL_TILES_BATHTILE_RJJ_TYPE(constants):
    return item_type('val.Tiles_BathTile.RJJ')

@mproperty
def VAL_TILES_BRICKS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Bricks.RJJ')

@mproperty
def VAL_TILES_CHECKS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Checks.RJJ')

@mproperty
def VAL_TILES_CORNERLESS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Cornerless.RJJ')

@mproperty
def VAL_TILES_CUBES_RJJ_TYPE(constants):
    return item_type('val.Tiles_Cubes.RJJ')

@mproperty
def VAL_TILES_DASHLINE_RJJ_TYPE(constants):
    return item_type('val.Tiles_DashLine.RJJ')

@mproperty
def VAL_TILES_DIAMONDDECK_RJJ_TYPE(constants):
    return item_type('val.Tiles_DiamondDeck.RJJ')

@mproperty
def VAL_TILES_FISHSCALES_RJJ_TYPE(constants):
    return item_type('val.Tiles_FishScales.RJJ')

@mproperty
def VAL_TILES_HEXTILE_RJJ_TYPE(constants):
    return item_type('val.Tiles_HexTile.RJJ')

@mproperty
def VAL_TILES_LATTICE1_RJJ_TYPE(constants):
    return item_type('val.Tiles_Lattice1.RJJ')

@mproperty
def VAL_TILES_LATTICE2_RJJ_TYPE(constants):
    return item_type('val.Tiles_Lattice2.RJJ')

@mproperty
def VAL_TILES_LATTICE3_RJJ_TYPE(constants):
    return item_type('val.Tiles_Lattice3.RJJ')

@mproperty
def VAL_TILES_MOSAIC_RJJ_TYPE(constants):
    return item_type('val.Tiles_Mosaic.RJJ')

@mproperty
def VAL_TILES_OCTTILE_RJJ_TYPE(constants):
    return item_type('val.Tiles_OctTile.RJJ')

@mproperty
def VAL_TILES_PARQUET_RJJ_TYPE(constants):
    return item_type('val.Tiles_Parquet.RJJ')

@mproperty
def VAL_TILES_PAVING_RJJ_TYPE(constants):
    return item_type('val.Tiles_Paving.RJJ')

@mproperty
def VAL_TILES_PLAID_RJJ_TYPE(constants):
    return item_type('val.Tiles_Plaid.RJJ')

@mproperty
def VAL_TILES_PLANKS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Planks.RJJ')

@mproperty
def VAL_TILES_RIBS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Ribs.RJJ')

@mproperty
def VAL_TILES_ROUNDEDTILE_RJJ_TYPE(constants):
    return item_type('val.Tiles_RoundedTile.RJJ')

@mproperty
def VAL_TILES_SHINGLES_RJJ_TYPE(constants):
    return item_type('val.Tiles_Shingles.RJJ')

@mproperty
def VAL_TILES_SPOTS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Spots.RJJ')

@mproperty
def VAL_TILES_STAMPED_RJJ_TYPE(constants):
    return item_type('val.Tiles_Stamped.RJJ')

@mproperty
def VAL_TILES_TACOS_RJJ_TYPE(constants):
    return item_type('val.Tiles_Tacos.RJJ')

@mproperty
def VAL_TILES_TARTAN_RJJ_TYPE(constants):
    return item_type('val.Tiles_TarTan.RJJ')

@mproperty
def VAL_TILES_TILER_RJJ_TYPE(constants):
    return item_type('val.Tiles_Tiler.RJJ')

@mproperty
def VAL_TILES_TRICHECKS_RJJ_TYPE(constants):
    return item_type('val.Tiles_TriChecks.RJJ')

@mproperty
def VAL_TILES_TRIHEXES_RJJ_TYPE(constants):
    return item_type('val.Tiles_TriHexes.RJJ')

@mproperty
def VAL_TILES_TRITILE_RJJ_TYPE(constants):
    return item_type('val.Tiles_TriTile.RJJ')

@mproperty
def VAL_TILES_WALL_RJJ_TYPE(constants):
    return item_type('val.Tiles_Wall.RJJ')

@mproperty
def VAL_WATER_DRIPDROP_RJJ_TYPE(constants):
    return item_type('val.Water_DripDrop.RJJ')

@mproperty
def VAL_WATER_RAIN_RJJ_TYPE(constants):
    return item_type('val.Water_Rain.RJJ')

@mproperty
def VAL_WATER_RIPPLES_RJJ_TYPE(constants):
    return item_type('val.Water_Ripples.RJJ')

@mproperty
def VAL_WATER_SURF_RJJ_TYPE(constants):
    return item_type('val.Water_Surf.RJJ')

@mproperty
def VAL_WATER_WAVES_RJJ_TYPE(constants):
    return item_type('val.Water_Waves.RJJ')

@mproperty
def VAL_WATER_WINDYWAVES_RJJ_TYPE(constants):
    return item_type('val.Water_WindyWaves.RJJ')

@mproperty
def VAL_WAVEFORMS_BIASGAIN_RJJ_TYPE(constants):
    return item_type('val.Waveforms_BiasGain.RJJ')

@mproperty
def VAL_WAVEFORMS_FRESNEL_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Fresnel.RJJ')

@mproperty
def VAL_WAVEFORMS_GAMMA_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Gamma.RJJ')

@mproperty
def VAL_WAVEFORMS_GAUSSIAN_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Gaussian.RJJ')

@mproperty
def VAL_WAVEFORMS_IMPULSE_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Impulse.RJJ')

@mproperty
def VAL_WAVEFORMS_NOISE_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Noise.RJJ')

@mproperty
def VAL_WAVEFORMS_RAMP_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Ramp.RJJ')

@mproperty
def VAL_WAVEFORMS_ROUNDED_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Rounded.RJJ')

@mproperty
def VAL_WAVEFORMS_SCURVE_RJJ_TYPE(constants):
    return item_type('val.Waveforms_SCurve.RJJ')

@mproperty
def VAL_WAVEFORMS_SAWTOOTH_RJJ_TYPE(constants):
    return item_type('val.Waveforms_SawTooth.RJJ')

@mproperty
def VAL_WAVEFORMS_SCALLOP_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Scallop.RJJ')

@mproperty
def VAL_WAVEFORMS_SINE_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Sine.RJJ')

@mproperty
def VAL_WAVEFORMS_SMOOTH_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Smooth.RJJ')

@mproperty
def VAL_WAVEFORMS_SMOOTHIMPULSE_RJJ_TYPE(constants):
    return item_type('val.Waveforms_SmoothImpulse.RJJ')

@mproperty
def VAL_WAVEFORMS_SMOOTHSTEP_RJJ_TYPE(constants):
    return item_type('val.Waveforms_SmoothStep.RJJ')

@mproperty
def VAL_WAVEFORMS_STAIRCASE_RJJ_TYPE(constants):
    return item_type('val.Waveforms_Staircase.RJJ')

@mproperty
def VAL_NOISE_GABOR_TYPE(constants):
    return item_type('val.noise.gabor')

@mproperty
def VAL_NOISE_POISSON_TYPE(constants):
    return item_type('val.noise.poisson')

@mproperty
def VAL_WIREFRAME_TYPE(constants):
    return item_type('val.wireframe')

@mproperty
def VARIATIONTEXTURE_TYPE(constants):
    return item_type('variationTexture')

@mproperty
def VIDEOBLANK_TYPE(constants):
    return item_type('videoBlank')

@mproperty
def VIDEOCLIP_TYPE(constants):
    return item_type('videoClip')

@mproperty
def VIDEOSEQUENCE_TYPE(constants):
    return item_type('videoSequence')

@mproperty
def VIDEOSTILL_TYPE(constants):
    return item_type('videoStill')

@mproperty
def VMAPTEXTURE_TYPE(constants):
    return item_type('vmapTexture')

@mproperty
def VOLUME_TYPE(constants):
    return item_type('volume')

@mproperty
def WEAVE_TYPE(constants):
    return item_type('weave')

@mproperty
def WEIGHTCONTAINER_TYPE(constants):
    return item_type('weightContainer')

@mproperty
def WIDGET_TYPE(constants):
    return item_type('widget')

@mproperty
def WOOD_TYPE(constants):
    return item_type('wood')

@mproperty
def XFRMCORE_TYPE(constants):
    return item_type('xfrmcore')


