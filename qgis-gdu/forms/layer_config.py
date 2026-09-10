
class LayerConfig:
    config = {
        'programa':{
            'id':'programa_ab82fdd9_6fa8_4212_825b_70ba9592c751',
            'size':[420,150]
        },
        'actuacion':{
            'id':'actuacion_4a69e796_5bb5_477f_8056_c20b72208103',
            'size':[420,230]
        },
        'contratacion':{
            'id':'contratacion_83647379_36cc_4e5d_a5fe_4c6da2905cc8',
            'size':[420,320]
        },
        'intervencion':{
            'id':'intervencion_7669b28c_b9e1_404b_98db_8ec06fba3ecd',
            'size':[496,670],
            'nn': [
                {
                    'id':'plano_mensura_intervencion_195b14c4_f4cc_4ea5_a179_653aa8ea15dc_idintervencion_intervencion_7669b28c_b9e1_404b_98db_8ec06fba3ecd_id',
                    'tabla_intermedia':'plano_mensura_intervencion',
                    'tabla_final':'plano_mensura',
                    #relacion entre t. intermedia y t. final
                    'id_relacion_tabla_final': 'plano_mensura_intervencion_195b14c4_f4cc_4ea5_a179_653aa8ea15dc_idplano_plano_mensura_7ecf3100_ba58_4e6b_837e_d9c17ee7547e_id',
                    'element':'pm', #referencia al elemento del form que muestra los items
                    'dirty_field':'nombre'
                },
                {
                    'id':'intervencion_inspector_bfead406_5bd9_4a32_be3a_70418e866e25_idintervencion_intervencion_7669b28c_b9e1_404b_98db_8ec06fba3ecd_id',
                    'tabla_intermedia':'intervencion_inspector',
                    'tabla_final':'inspector',
                    #relacion entre t. intermedia y t. final
                    'id_relacion_tabla_final': 'intervencion_inspector_bfead406_5bd9_4a32_be3a_70418e866e25_idinspector_inspector_c01e6b01_d78b_4d8f_8775_a9b29e551fdb_id',
                    'element':'inspectores', #referencia al elemento del form que muestra los items
                    'dirty_field':'nombre'
                },
                {
                    'id':'intervencion_ejecutor_ce3138fc_e874_48ae_afb9_91073d34fee3_id_intervencion_intervencion_7669b28c_b9e1_404b_98db_8ec06fba3ecd_id',
                    'tabla_intermedia':'intervencion_ejecutor',
                    'tabla_final':'ejecutor',
                    #relacion entre t. intermedia y t. final
                    'id_relacion_tabla_final': 'intervencion_ejecutor_ce3138fc_e874_48ae_afb9_91073d34fee3_id_ejecutor_ejecutor_e09fd31f_2a1d_40bc_ba5a_6e186cc4a460_id',
                    'element':'ejecutores', #referencia al elemento del form que muestra los items
                    'dirty_field':'nombre'
                }
            ]
        },
        'tierra':{
            'id':'tierra_d651e31d_ddd2_4ad6_a544_20308cb56acc',
            'size':[1280,630],
            'nn':[#relaciones NN que controla el form, si no tiene deberia solo abrir el form con 
                # las dimensiones especificas y listo
                {   
                    #relacion entre la tabla inicial y la intermedia
                    'id':'plano_mensura_tierra_f91a95a3_79e3_4c7d_a8b6_178eb85571b5_idtierra_tierra_d651e31d_ddd2_4ad6_a544_20308cb56acc_id',#id de la relacion con la tabla intermedia
                    'tabla_intermedia':'plano_mensura_tierra',#tabla intermedia
                    'tabla_final':'plano_mensura',
                    #relacion entre t. intermedia y t. final
                    'id_relacion_tabla_final': 'plano_mensura_tierra_f91a95a3_79e3_4c7d_a8b6_178eb85571b5_idplano_plano_mensura_7ecf3100_ba58_4e6b_837e_d9c17ee7547e_id',
                    'element':'pm', #referencia al elemento del form que muestra los items
                    #id?? si es id se puede usar como prefijo para botones y demas
                    #guardar la relacion entre la tabla intermedia y la final????

                    # campo para modificar y que el feature quede marcado como "dirty", así es guardado
                    # HORRIBLE!!! Buscar otra forma mejor...
                    'dirty_field':'oferente'
                    
                    
                }
                # 
                # 
            ]
        },
        'uf':{
            'id':'uf_6eee47a9_60be_407a_bbca_a3fd8916a24f',
            'size':[420,470]
        },
        'vivienda_punto':{
            'id':'vivienda_punto_cc842d74_4890_4d97_b267_8983d9ec8da8',
            'size':[600,600]
        },
        'localidad':{
            'id':'localidad_2cb926e9_2bca_452a_aa59_83e5f932b1fb',
            'size':[420,280]
        },
        'manzana':{
            'id':'manzana_eb65c611_3536_46ba_af46_765733213da9',
            'size':[420,150]
        },
        'parcela':{
            'id':'parcela_7b137359_7fff_4d9e_9482_ae6ee87e8422',
            'size':[600,350]
        },
        'dpto1':{
            'id':'dpto_de6d318a_7293_44a2_b554_8a754c9a9aca',
            'size':[600,350]
        },
        'dpto2':{
            'id':'dpto_d60b2dfc_5df6_4945_85d9_20c9b907977a',
            'size':[600,350]
        },
        'dpto3':{
            'id':'dpto_38ba1385_55a9_49d7_bb16_d31eca3316b2',
            'size':[600,350]
        },
        'dpto4':{
            'id':'dpto_69a6998c_3264_455b_a349_5f74bfb89f2c',
            'size':[600,350]
        },
        'dpto5':{
            'id':'dpto_6c9bf516_eba6_4bd8_96dd_6112ab728f80',
            'size':[600,350]
        },
        'dpto6':{
            'id':'dpto_0b90abae_bebf_42a5_91f2_de1958d80e35',
            'size':[600,350]
        },
        'dpto7':{
            'id':'dpto_e72b7b1a_f45e_4393_85e1_e20f4546fd47',
            'size':[600,350]
        },
        'dpto8':{
            'id':'dpto_5d5c7042_7274_4984_b2ba_382182ca8463',
            'size':[600,350]
        },
        'dpto9':{
            'id':'dpto_c5f5f561_e9bc_448f_8ff6_49a565df2f8d',
            'size':[600,350]
        },
        'dpto10':{
            'id':'dpto_c6c2cdf7_ee9c_4c59_9273_1352a8516e48',
            'size':[600,350]
        },
        'dpto11':{
            'id':'dpto_dc275bdd_67cd_4b81_9b72_52b98d31f3a0',
            'size':[600,350]
        },
        'dpto12':{
            'id':'dpto_75122e4a_0a19_4f1d_9bfc_9484116e8809',
            'size':[600,350]
        },
        'dpto13':{
            'id':'dpto_21527068_0d41_4226_8db0_bb27bdefeb25',
            'size':[600,350]
        },
        'dpto14':{
            'id':'dpto_df80ec6f_07a7_4640_be7a_f49382a324f0',
            'size':[600,350]
        },
        'dpto15':{
            'id':'dpto_52a62761_b979_439c_bfea_416d4fde0847',
            'size':[600,350]
        },
        'dpto16':{
            'id':'dpto_e98da5fc_a2ef_4b8d_948f_48cb56b66219',
            'size':[600,350]
        },
        'dpto17':{
            'id':'dpto_5411da3b_c996_4e15_94ab_e15b8e66ead8',
            'size':[600,350]
        },
        'dpto18':{
            'id':'dpto_c3eb1304_d35c_409d_88ba_786683cadc5a',
            'size':[600,350]
        },
        'dpto19':{
            'id':'dpto_0fd515b9_a65b_47a1_bfa4_5deb18b4a057',
            'size':[600,350]
        },
        'dpto20':{
            'id':'dpto_e3b79b25_6443_4a76_b0de_60c804821ef1',
            'size':[600,350]
        },
        'dpto21':{
            'id':'dpto_25874ad4_1f71_428a_ae23_37f2e722b9ff',
            'size':[600,350]
        },
        'dpto22':{
            'id':'dpto_909e445b_4905_4b62_81a9_81df9faf057c',
            'size':[600,350]
        },
        'dpto23':{
            'id':'dpto_b0d41e64_f13a_405e_a8ad_baa0f161af7c',
            'size':[600,350]
        },
        'dpto24':{
            'id':'dpto_ca273a76_da06_4c21_9cc5_0a90ea4909c7',
            'size':[600,350]
        },
        'dpto25':{
            'id':'dpto_8284cb1c_77a7_472c_82e2_067256a857d8',
            'size':[600,350]
        },
       
        'rcia_norte':{
            'id':'Región_10_fb830d15_36dc_4a4e_87f5_9f8c27187771',
            'size':[600,350]
        },
        'rcia_sur':{
            'id':'Resistencia_Norte_bb5baf92_13d3_41f4_9aef_a23d59249c8f',
            'size':[600,350]
        },
        'rcia_este':{
            'id':'Resistencia_Sur_4e57a0d9_367a_4808_a0dc_ac4ee35b4bcf',
            'size':[600,350]
        },
        'rcia_oeste':{
            'id':'Resistencia_Este_5a462fa0_e2f3_40fd_b3f5_cdc8b0e8d15a',
            'size':[600,350]
        },
        'parcela_expropiada':{
            'id':'parcela_expropiada_9fc6d546_6e21_4229_8d05_50f8ff43ff87',
            'size':[610,550]
        },
        'barrio':{
            'id':'barrio_137b1178_a182_4f18_97c2_93299902a23f',
            'size':[420,150]
        },
        'calle':{
            'id':'calle_f96527ee_dd8c_4063_9e62_fcf3249d2b38',
            'size':[420,150]
        },
        'inspector':{
            'id':'inspector_c01e6b01_d78b_4d8f_8775_a9b29e551fdb',
            'size':[420,130]
        },
        'plano_mensura':{
            'id':'plano_mensura_7ecf3100_ba58_4e6b_837e_d9c17ee7547e',
            'size':[420,360],
        },
        'plano_mensura_tierra':{
            'id':'plano_mensura_tierra_f91a95a3_79e3_4c7d_a8b6_178eb85571b5',
            'size':[0,0]
        },
        'tipo_contratacion':{
            'id':'tipo_contratacion_b26c76be_71cb_41fe_8afa_4a2f588dde62',
            'size':[420,130]
        },
        'tipo_ejecutor':{
            'id':'tipo_ejecutor_ef569548_93c0_4cbb_8130_3c417fa1c415',
            'size':[420,130]
        },
        'tipo_estado':{
            'id':'tipo_estado_4929d108_31a1_4f2b_ae47_b5ae9ce6995a',
            'size':[420,130]
        },
        'tipo_intervencion':{
            'id':'tipo_intervencion_6abf9aea_9219_4325_9826_ffb8f2a9ab7b',
            'size':[420,130]
        },
        'tipo_uf':{
            'id':'tipo_uf_bf53d84e_4688_45a3_9c2f_e82d5c5c5425',
            'size':[420,130]
        },
        # 'tipo_gestion_tierra':{
        #     'id':'tipo_gestion_tierra_c3c0987e_b611_4a57_9fcd_cc0497688450',
        #     'size':[420,130]
        # },
        'objeto_expropiacion':{
            'id':'objeto_expropiacion_ab0f046e_092d_48e4_aac6_967d8c4cc818',
            'size':[420,130]
        },
        'estado_gestion_expropiacion':{
            'id':'estado_gestion_expropiacion_a92b4ba4_f58e_46f2_9893_43f1678679f0',
            'size':[420,130]
        },
        'adjudicacion_beneficiario':{
            'id':'adjudicacion_beneficiario_c266c3ab_5fad_4c32_b38a_3bca444516dc',
            'size':[420,190]
        },
        'destino_parcela':{
            'id':'destino_parcela_b6788664_53be_4b7c_b334_d1de62ffcdba',
            'size':[420,130]
        },
        'tipo_doc_probatoria':{
            'id':'tipo_doc_probatoria_c899332e_072f_4877_b0ce_0d5ff92733b1',
            'size':[420,130]
        },
        'tierra_destino':{
            'id':'tierra_destino_fb7278ef_03ca_4525_9885_ef6c5e9c0e15',
            'size':[420,130]
        },
        'ejecutor':{
            'id':'ejecutor_e09fd31f_2a1d_40bc_ba5a_6e186cc4a460',
            'size':[420,320]
        },
        'intervencion_ejecutor':{
            'id':'intervencion_ejecutor_ce3138fc_e874_48ae_afb9_91073d34fee3',
            'size':[0,0]
        },
        # 'objeto_expropiacion':{
        #     'id':'objeto_expropiacion_ab0f046e_092d_48e4_aac6_967d8c4cc818',
        #     'size':[0,0]
        # },
        'expropiacion':{
            'id':'expropiacion_595f85fd_b4e7_4524_93bd_f23c6ceba1ee',
            'size':[420,330]
        },
        'resolucion_costos':{
            'id':'resolucion_costos_e8c68b5f_ae5e_417d_9656_6a2b6b2ea77e',
            'size':[400,190]
        },
        # 'gestion_tierra':{
        #     'id':'gestion_tierra_650817c5_b483_4ba4_8903_7364c6f25d4e',
        #     'size':[420,230]
        # },
        'plano_mensura_intervencion':{
            'id':'plano_mensura_intervencion_195b14c4_f4cc_4ea5_a179_653aa8ea15dc',
            'size':[420,180]
        },
        'intervencion_inspector':{
            'id':'intervencion_inspector_bfead406_5bd9_4a32_be3a_70418e866e25',
            'size':[420,180]
        },
        'pre_adjudicatario_dispersa':{
            'id': 'pre_adjudicatario_dispersa_252a373b_54ba_4105_9a12_27365799b1d8',
            'size':[420,500]
        }

        
        # ,
        # 'xxxxxxxx':{
        #     'id':'',
        #     'size':[0,0]
        # }
    }
    def find(self,id):
        for name,l in self.config.items():
            if l['id']==id:
                return l
        return None

    def get(self,layer):
        if layer in self.config:
            return self.config[layer]
        return None
