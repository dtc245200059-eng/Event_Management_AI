# EventAI Pro — Phase 10B-R: Authoritative Test Node ID Inventory

**Document ID**: `DOC-DEPLOY-PHASE10BR-NODEID-002`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Total Collected Tests**: 218 Tests across 12 Files  
**Verification Method**: Output of `pytest --collect-only -q`  
**Date**: 2026-10-29  

---

## 1. Executive Summary

This document lists every single one of the 218 test node identifiers discovered by pytest in the project virtual environment (`D:\Event_Management_AI\.venv`), definitively reconciling the test suite identity.

---

## 1. `tests/test_ai_services.py` (9 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_ai_services.py::test_rag_fallback_mock_engine` | Rag fallback mock engine |
| 02 | `tests/test_ai_services.py::test_recommendation_engine` | Recommendation engine |
| 03 | `tests/test_ai_services.py::test_predictive_attendance_calculation` | Predictive attendance calculation |
| 04 | `tests/test_ai_services.py::test_question_analysis` | Question analysis |
| 05 | `tests/test_ai_services.py::test_rag_context_and_free_event_retrieval` | Rag context and free event retrieval |
| 06 | `tests/test_ai_services.py::test_chat_api_endpoint` | Chat api endpoint |
| 07 | `tests/test_ai_services.py::test_ai_notification_generator` | Ai notification generator |
| 08 | `tests/test_ai_services.py::test_ai_feedback_summary_groups` | Ai feedback summary groups |
| 09 | `tests/test_ai_services.py::test_rag_faq_retrieval` | Rag faq retrieval |


## 2. `tests/test_auth.py` (7 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_auth.py::test_user_password_hashing` | User password hashing |
| 02 | `tests/test_auth.py::test_user_roles` | User roles |
| 03 | `tests/test_auth.py::test_login_success` | Login success |
| 04 | `tests/test_auth.py::test_login_failure_wrong_password` | Login failure wrong password |
| 05 | `tests/test_auth.py::test_admin_create_staff_user` | Admin create staff user |
| 06 | `tests/test_auth.py::test_admin_change_user_role` | Admin change user role |
| 07 | `tests/test_auth.py::test_non_admin_cannot_manage_users` | Non admin cannot manage users |


## 3. `tests/test_csrf_security.py` (26 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_csrf_security.py::test_csrf_valid_token_accepted_on_form_post` | Csrf valid token accepted on form post |
| 02 | `tests/test_csrf_security.py::test_csrf_missing_token_rejected_with_400` | Csrf missing token rejected with 400 |
| 03 | `tests/test_csrf_security.py::test_csrf_invalid_token_rejected_with_400` | Csrf invalid token rejected with 400 |
| 04 | `tests/test_csrf_security.py::test_csrf_expired_token_rejected_with_400` | Csrf expired token rejected with 400 |
| 05 | `tests/test_csrf_security.py::test_csrf_token_from_another_session_rejected` | Csrf token from another session rejected |
| 06 | `tests/test_csrf_security.py::test_csrf_json_ajax_without_token_returns_json_400` | Csrf json ajax without token returns json 400 |
| 07 | `tests/test_csrf_security.py::test_csrf_json_ajax_with_valid_header_accepted` | Csrf json ajax with valid header accepted |
| 08 | `tests/test_csrf_security.py::test_csrf_admin_user_management_protected` | Csrf admin user management protected |
| 09 | `tests/test_csrf_security.py::test_csrf_event_management_protected` | Csrf event management protected |
| 10 | `tests/test_csrf_security.py::test_csrf_ticket_registration_protected` | Csrf ticket registration protected |
| 11 | `tests/test_csrf_security.py::test_csrf_profile_update_protected` | Csrf profile update protected |
| 12 | `tests/test_csrf_security.py::test_csrf_password_change_protected` | Csrf password change protected |
| 13 | `tests/test_csrf_security.py::test_csrf_checkin_quick_actions_protected` | Csrf checkin quick actions protected |
| 14 | `tests/test_csrf_security.py::test_csrf_ai_chat_protected` | Csrf ai chat protected |
| 15 | `tests/test_csrf_security.py::test_csrf_cross_origin_request_with_invalid_origin_rejected` | Csrf cross origin request with invalid origin rejected |
| 16 | `tests/test_csrf_security.py::test_csrf_logout_post_with_valid_token_succeeds` | Csrf logout post with valid token succeeds |
| 17 | `tests/test_csrf_security.py::test_csrf_logout_post_without_token_rejected_with_400` | Csrf logout post without token rejected with 400 |
| 18 | `tests/test_csrf_security.py::test_csrf_cache_isolation_headers_present_on_html` | Csrf cache isolation headers present on html |
| 19 | `tests/test_csrf_security.py::test_csrf_token_not_leaked_in_sitemap_or_robots` | Csrf token not leaked in sitemap or robots |
| 20 | `tests/test_csrf_security.py::test_csrf_token_not_leaked_in_public_jsonld` | Csrf token not leaked in public jsonld |
| 21 | `tests/test_csrf_security.py::test_csrf_logout_get_does_not_terminate_session` | Csrf logout get does not terminate session |
| 22 | `tests/test_csrf_security.py::test_csrf_logout_post_with_invalid_token_rejected_with_400` | Csrf logout post with invalid token rejected with 400 |
| 23 | `tests/test_csrf_security.py::test_csrf_logout_post_with_expired_token_rejected_with_400` | Csrf logout post with expired token rejected with 400 |
| 24 | `tests/test_csrf_security.py::test_csrf_anonymous_and_authenticated_cache_isolation` | Csrf anonymous and authenticated cache isolation |
| 25 | `tests/test_csrf_security.py::test_csrf_cross_user_qr_access_forbidden` | Csrf cross user qr access forbidden |
| 26 | `tests/test_csrf_security.py::test_csrf_route_inventory_no_mutating_get` | Csrf route inventory no mutating get |


## 4. `tests/test_event_schema.py` (32 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_event_schema.py::test_published_event_produces_valid_event_schema` | Published event produces valid event schema |
| 02 | `tests/test_event_schema.py::test_schema_event_name` | Schema event name |
| 03 | `tests/test_event_schema.py::test_schema_event_description_sanitized` | Schema event description sanitized |
| 04 | `tests/test_event_schema.py::test_schema_event_canonical_url` | Schema event canonical url |
| 05 | `tests/test_event_schema.py::test_schema_iso8601_start_date` | Schema iso8601 start date |
| 06 | `tests/test_event_schema.py::test_schema_iso8601_end_date` | Schema iso8601 end date |
| 07 | `tests/test_event_schema.py::test_format_iso8601_timezone_handling` | Format iso8601 timezone handling |
| 08 | `tests/test_event_schema.py::test_invalid_date_interval_normalized` | Invalid date interval normalized |
| 09 | `tests/test_event_schema.py::test_physical_event_location` | Physical event location |
| 10 | `tests/test_event_schema.py::test_online_event_location` | Online event location |
| 11 | `tests/test_event_schema.py::test_hybrid_event_location` | Hybrid event location |
| 12 | `tests/test_event_schema.py::test_missing_location_fallback` | Missing location fallback |
| 13 | `tests/test_event_schema.py::test_event_status_mapping_scheduled` | Event status mapping scheduled |
| 14 | `tests/test_event_schema.py::test_cancelled_event_schema` | Cancelled event schema |
| 15 | `tests/test_event_schema.py::test_draft_event_excluded_from_schema_builder` | Draft event excluded from schema builder |
| 16 | `tests/test_event_schema.py::test_anonymous_cannot_view_draft_event` | Anonymous cannot view draft event |
| 17 | `tests/test_event_schema.py::test_authorized_draft_preview_does_not_emit_jsonld` | Authorized draft preview does not emit jsonld |
| 18 | `tests/test_event_schema.py::test_ticket_offers_free_ticket` | Ticket offers free ticket |
| 19 | `tests/test_event_schema.py::test_ticket_offers_paid_ticket` | Ticket offers paid ticket |
| 20 | `tests/test_event_schema.py::test_ticket_offers_sold_out` | Ticket offers sold out |
| 21 | `tests/test_event_schema.py::test_multiple_ticket_types_array` | Multiple ticket types array |
| 22 | `tests/test_event_schema.py::test_missing_price_safe_fallback` | Missing price safe fallback |
| 23 | `tests/test_event_schema.py::test_relative_image_url_made_absolute` | Relative image url made absolute |
| 24 | `tests/test_event_schema.py::test_organizer_structure` | Organizer structure |
| 25 | `tests/test_event_schema.py::test_missing_optional_fields_handled_gracefully` | Missing optional fields handled gracefully |
| 26 | `tests/test_event_schema.py::test_json_escaping_and_valid_syntax` | Json escaping and valid syntax |
| 27 | `tests/test_event_schema.py::test_xss_script_breakout_prevention` | Xss script breakout prevention |
| 28 | `tests/test_event_schema.py::test_vietnamese_unicode_in_schema` | Vietnamese unicode in schema |
| 29 | `tests/test_event_schema.py::test_no_duplicate_event_schema` | No duplicate event schema |
| 30 | `tests/test_event_schema.py::test_breadcrumblist_schema` | Breadcrumblist schema |
| 31 | `tests/test_event_schema.py::test_breadcrumblist_builder_standalone` | Breadcrumblist builder standalone |
| 32 | `tests/test_event_schema.py::test_no_private_tokens_or_pii_in_schema` | No private tokens or pii in schema |


## 5. `tests/test_multi_agent.py` (10 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_multi_agent.py::test_agent_message_protocol` | Agent message protocol |
| 02 | `tests/test_multi_agent.py::test_message_bus_audit_log` | Message bus audit log |
| 03 | `tests/test_multi_agent.py::test_sql_tool_database_queries` | Sql tool database queries |
| 04 | `tests/test_multi_agent.py::test_vector_search_tool_knowledge` | Vector search tool knowledge |
| 05 | `tests/test_multi_agent.py::test_requirement_agent_extraction` | Requirement agent extraction |
| 06 | `tests/test_multi_agent.py::test_retrieval_agent_execution` | Retrieval agent execution |
| 07 | `tests/test_multi_agent.py::test_critic_agent_approve_and_reject` | Critic agent approve and reject |
| 08 | `tests/test_multi_agent.py::test_full_orchestrator_workflow_and_trace` | Full orchestrator workflow and trace |
| 09 | `tests/test_multi_agent.py::test_orchestrator_retry_loop_on_critique` | Orchestrator retry loop on critique |
| 10 | `tests/test_multi_agent.py::test_benchmark_suite_10_cases` | Benchmark suite 10 cases |


## 6. `tests/test_notifications_and_feedback.py` (4 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_notifications_and_feedback.py::test_organizer_role_access` | Organizer role access |
| 02 | `tests/test_notifications_and_feedback.py::test_notification_creation_and_recipient_calc` | Notification creation and recipient calc |
| 03 | `tests/test_notifications_and_feedback.py::test_attendee_notification_inbox` | Attendee notification inbox |
| 04 | `tests/test_notifications_and_feedback.py::test_feedback_submission_and_sentiment_rating` | Feedback submission and sentiment rating |


## 7. `tests/test_phase2_5_security.py` (19 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_phase2_5_security.py::test_login_page_does_not_expose_credentials` | Login page does not expose credentials |
| 02 | `tests/test_phase2_5_security.py::test_login_and_register_pages_have_noindex` | Login and register pages have noindex |
| 03 | `tests/test_phase2_5_security.py::test_error_pages_have_noindex` | Error pages have noindex |
| 04 | `tests/test_phase2_5_security.py::test_anonymous_cannot_access_private_qr_static` | Anonymous cannot access private qr static |
| 05 | `tests/test_phase2_5_security.py::test_cross_user_ticket_qr_access_denied` | Cross user ticket qr access denied |
| 06 | `tests/test_phase2_5_security.py::test_authorized_owner_can_access_own_ticket_qr` | Authorized owner can access own ticket qr |
| 07 | `tests/test_phase2_5_security.py::test_staff_and_admin_can_access_any_ticket_qr` | Staff and admin can access any ticket qr |
| 08 | `tests/test_phase2_5_security.py::test_anonymous_cannot_access_draft_event` | Anonymous cannot access draft event |
| 09 | `tests/test_phase2_5_security.py::test_regular_attendee_cannot_access_draft_event` | Regular attendee cannot access draft event |
| 10 | `tests/test_phase2_5_security.py::test_admin_and_creator_can_preview_draft_event` | Admin and creator can preview draft event |
| 11 | `tests/test_phase2_5_security.py::test_public_published_event_is_accessible_to_all` | Public published event is accessible to all |
| 12 | `tests/test_phase2_5_security.py::test_cancelled_event_has_noindex_and_closed_booking` | Cancelled event has noindex and closed booking |
| 13 | `tests/test_phase2_5_security.py::test_http_security_headers_present` | Http security headers present |
| 14 | `tests/test_phase2_5_security.py::test_production_config_cookie_security` | Production config cookie security |
| 15 | `tests/test_phase2_5_security.py::test_staging_config_profile` | Staging config profile |
| 16 | `tests/test_phase2_5_security.py::test_cross_origin_state_changing_request_protection` | Cross origin state changing request protection |
| 17 | `tests/test_phase2_5_security.py::test_zero_state_changing_get_routes` | Zero state changing get routes |
| 18 | `tests/test_phase2_5_security.py::test_seo_helpers_creator_lazy_load_exception_handling` | Seo helpers creator lazy load exception handling |
| 19 | `tests/test_phase2_5_security.py::test_csrf_cookie_same_site_defense_in_depth` | Csrf cookie same site defense in depth |


## 8. `tests/test_phase3d_performance.py` (27 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_phase3d_performance.py::TestResourceHintsAndLoading::test_base_template_has_preconnect_hints` | Testresourcehintsandloading::base template has preconnect hints |
| 02 | `tests/test_phase3d_performance.py::TestResourceHintsAndLoading::test_base_template_has_dns_prefetch_hints` | Testresourcehintsandloading::base template has dns prefetch hints |
| 03 | `tests/test_phase3d_performance.py::TestResourceHintsAndLoading::test_application_scripts_have_defer_attribute` | Testresourcehintsandloading::application scripts have defer attribute |
| 04 | `tests/test_phase3d_performance.py::TestLcpAndLazyLoading::test_homepage_hero_carousel_lcp_first_image_priority` | Testlcpandlazyloading::homepage hero carousel lcp first image priority |
| 05 | `tests/test_phase3d_performance.py::TestLcpAndLazyLoading::test_homepage_hero_carousel_subsequent_images_lazy_loaded` | Testlcpandlazyloading::homepage hero carousel subsequent images lazy loaded |
| 06 | `tests/test_phase3d_performance.py::TestLcpAndLazyLoading::test_homepage_below_the_fold_cards_lazy_loaded` | Testlcpandlazyloading::homepage below the fold cards lazy loaded |
| 07 | `tests/test_phase3d_performance.py::TestLcpAndLazyLoading::test_event_detail_hero_banner_high_priority_and_never_lazy` | Testlcpandlazyloading::event detail hero banner high priority and never lazy |
| 08 | `tests/test_phase3d_performance.py::TestLcpAndLazyLoading::test_events_catalog_images_loading_strategy` | Testlcpandlazyloading::events catalog images loading strategy |
| 09 | `tests/test_phase3d_performance.py::TestLayoutStability::test_image_tags_have_explicit_width_and_height` | Testlayoutstability::image tags have explicit width and height |
| 10 | `tests/test_phase3d_performance.py::TestLayoutStability::test_css_aspect_ratio_rules_exist` | Testlayoutstability::css aspect ratio rules exist |
| 11 | `tests/test_phase3d_performance.py::TestAnimationAndInteractionEfficiency::test_javascript_slider_has_reduced_motion_check` | Testanimationandinteractionefficiency::javascript slider has reduced motion check |
| 12 | `tests/test_phase3d_performance.py::TestAnimationAndInteractionEfficiency::test_javascript_slider_uses_intersection_observer` | Testanimationandinteractionefficiency::javascript slider uses intersection observer |
| 13 | `tests/test_phase3d_performance.py::TestAnimationAndInteractionEfficiency::test_javascript_slider_uses_page_visibility_api` | Testanimationandinteractionefficiency::javascript slider uses page visibility api |
| 14 | `tests/test_phase3d_performance.py::TestAnimationAndInteractionEfficiency::test_css_gpu_compositing_will_change_rules` | Testanimationandinteractionefficiency::css gpu compositing will change rules |
| 15 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_carousel_indicators_have_descriptive_accessible_names` | Testaccessibilitycompliance::carousel indicators have descriptive accessible names |
| 16 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_carousel_prev_next_controls_have_accessible_labels` | Testaccessibilitycompliance::carousel prev next controls have accessible labels |
| 17 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_search_forms_have_accessible_search_role_and_labels` | Testaccessibilitycompliance::search forms have accessible search role and labels |
| 18 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_events_category_select_has_aria_label` | Testaccessibilitycompliance::events category select has aria label |
| 19 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_ai_chat_modal_and_controls_accessibility` | Testaccessibilitycompliance::ai chat modal and controls accessibility |
| 20 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_css_visible_focus_indicators` | Testaccessibilitycompliance::css visible focus indicators |
| 21 | `tests/test_phase3d_performance.py::TestAccessibilityCompliance::test_css_reduced_motion_media_query_present` | Testaccessibilitycompliance::css reduced motion media query present |
| 22 | `tests/test_phase3d_performance.py::TestMobileFirstAndGpuPerformance::test_viewport_meta_tag_configured_for_mobile` | Testmobilefirstandgpuperformance::viewport meta tag configured for mobile |
| 23 | `tests/test_phase3d_performance.py::TestMobileFirstAndGpuPerformance::test_mobile_gpu_backdrop_blur_optimization_in_css` | Testmobilefirstandgpuperformance::mobile gpu backdrop blur optimization in css |
| 24 | `tests/test_phase3d_performance.py::TestSecurityBaselinePreservation::test_login_page_no_credentials_exposed` | Testsecuritybaselinepreservation::login page no credentials exposed |
| 25 | `tests/test_phase3d_performance.py::TestSecurityBaselinePreservation::test_anonymous_cannot_access_draft_event` | Testsecuritybaselinepreservation::anonymous cannot access draft event |
| 26 | `tests/test_phase3d_performance.py::TestSecurityBaselinePreservation::test_sitemap_xml_protocol_capped_at_max_urls` | Testsecuritybaselinepreservation::sitemap xml protocol capped at max urls |
| 27 | `tests/test_phase3d_performance.py::TestSecurityBaselinePreservation::test_robots_txt_remains_valid` | Testsecuritybaselinepreservation::robots txt remains valid |


## 9. `tests/test_seo_core_metadata.py` (23 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_seo_core_metadata.py::test_homepage_title_and_description` | Homepage title and description |
| 02 | `tests/test_seo_core_metadata.py::test_homepage_canonical_url` | Homepage canonical url |
| 03 | `tests/test_seo_core_metadata.py::test_homepage_og_and_twitter_cards` | Homepage og and twitter cards |
| 04 | `tests/test_seo_core_metadata.py::test_events_page_title_and_description` | Events page title and description |
| 05 | `tests/test_seo_core_metadata.py::test_events_page_canonical_url` | Events page canonical url |
| 06 | `tests/test_seo_core_metadata.py::test_events_page_strips_tracking_parameters` | Events page strips tracking parameters |
| 07 | `tests/test_seo_core_metadata.py::test_event_detail_dynamic_metadata` | Event detail dynamic metadata |
| 08 | `tests/test_seo_core_metadata.py::test_event_detail_meta_description_html_stripping` | Event detail meta description html stripping |
| 09 | `tests/test_seo_core_metadata.py::test_event_detail_meta_description_truncation` | Event detail meta description truncation |
| 10 | `tests/test_seo_core_metadata.py::test_event_detail_meta_description_fallback` | Event detail meta description fallback |
| 11 | `tests/test_seo_core_metadata.py::test_event_detail_canonical_url` | Event detail canonical url |
| 12 | `tests/test_seo_core_metadata.py::test_event_detail_og_type_and_image` | Event detail og type and image |
| 13 | `tests/test_seo_core_metadata.py::test_event_detail_relative_image_is_made_absolute` | Event detail relative image is made absolute |
| 14 | `tests/test_seo_core_metadata.py::test_event_detail_fallback_og_image` | Event detail fallback og image |
| 15 | `tests/test_seo_core_metadata.py::test_canonical_domain_configuration_override` | Canonical domain configuration override |
| 16 | `tests/test_seo_core_metadata.py::test_special_characters_in_metadata_are_escaped` | Special characters in metadata are escaped |
| 17 | `tests/test_seo_core_metadata.py::test_no_duplicate_metadata_tags` | No duplicate metadata tags |
| 18 | `tests/test_seo_core_metadata.py::test_homepage_semantic_heading_hierarchy` | Homepage semantic heading hierarchy |
| 19 | `tests/test_seo_core_metadata.py::test_events_page_semantic_heading_hierarchy` | Events page semantic heading hierarchy |
| 20 | `tests/test_seo_core_metadata.py::test_event_detail_semantic_heading_hierarchy` | Event detail semantic heading hierarchy |
| 21 | `tests/test_seo_core_metadata.py::test_security_baseline_auth_and_errors_retain_noindex` | Security baseline auth and errors retain noindex |
| 22 | `tests/test_seo_core_metadata.py::test_security_baseline_draft_event_is_protected` | Security baseline draft event is protected |
| 23 | `tests/test_seo_core_metadata.py::test_security_baseline_private_qr_remains_blocked` | Security baseline private qr remains blocked |


## 10. `tests/test_seo_sitemap_robots.py` (49 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_status_and_headers` | Testsitemapendpoint::sitemap status and headers |
| 02 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_xml_well_formed_and_namespace` | Testsitemapendpoint::sitemap xml well formed and namespace |
| 03 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_includes_homepage_and_events_catalog` | Testsitemapendpoint::sitemap includes homepage and events catalog |
| 04 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_includes_published_events` | Testsitemapendpoint::sitemap includes published events |
| 05 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_includes_ongoing_and_completed_events` | Testsitemapendpoint::sitemap includes ongoing and completed events |
| 06 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_strictly_excludes_draft_events` | Testsitemapendpoint::sitemap strictly excludes draft events |
| 07 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_strictly_excludes_cancelled_events` | Testsitemapendpoint::sitemap strictly excludes cancelled events |
| 08 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_excludes_private_and_admin_urls` | Testsitemapendpoint::sitemap excludes private and admin urls |
| 09 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_excludes_auth_urls` | Testsitemapendpoint::sitemap excludes auth urls |
| 10 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_loc_elements_are_absolute_urls` | Testsitemapendpoint::sitemap loc elements are absolute urls |
| 11 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_honors_canonical_domain_config` | Testsitemapendpoint::sitemap honors canonical domain config |
| 12 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_no_duplicate_urls` | Testsitemapendpoint::sitemap no duplicate urls |
| 13 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_no_query_parameters` | Testsitemapendpoint::sitemap no query parameters |
| 14 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_lastmod_format_and_accuracy` | Testsitemapendpoint::sitemap lastmod format and accuracy |
| 15 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_omits_lastmod_when_updated_at_none` | Testsitemapendpoint::sitemap omits lastmod when updated at none |
| 16 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_static_pages_omit_lastmod` | Testsitemapendpoint::sitemap static pages omit lastmod |
| 17 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_deterministic_ordering` | Testsitemapendpoint::sitemap deterministic ordering |
| 18 | `tests/test_seo_sitemap_robots.py::TestSitemapEndpoint::test_sitemap_handles_empty_events_database` | Testsitemapendpoint::sitemap handles empty events database |
| 19 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_status_and_content_type` | Testrobotstxtendpoint::robots status and content type |
| 20 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_user_agent_directive` | Testrobotstxtendpoint::robots user agent directive |
| 21 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_allows_root` | Testrobotstxtendpoint::robots allows root |
| 22 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_allows_static_assets` | Testrobotstxtendpoint::robots allows static assets |
| 23 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_disallows_admin` | Testrobotstxtendpoint::robots disallows admin |
| 24 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_disallows_checkin` | Testrobotstxtendpoint::robots disallows checkin |
| 25 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_disallows_qr_codes` | Testrobotstxtendpoint::robots disallows qr codes |
| 26 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_disallows_api` | Testrobotstxtendpoint::robots disallows api |
| 27 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_leaves_auth_unblocked` | Testrobotstxtendpoint::robots leaves auth unblocked |
| 28 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_sitemap_directive_points_to_sitemap_xml` | Testrobotstxtendpoint::robots sitemap directive points to sitemap xml |
| 29 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_honors_canonical_domain` | Testrobotstxtendpoint::robots honors canonical domain |
| 30 | `tests/test_seo_sitemap_robots.py::TestRobotsTxtEndpoint::test_robots_no_html_tags` | Testrobotstxtendpoint::robots no html tags |
| 31 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_is_event_indexable_statuses` | Testseohelpersunit::is event indexable statuses |
| 32 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_is_event_indexable_unindexable_statuses` | Testseohelpersunit::is event indexable unindexable statuses |
| 33 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_get_trusted_canonical_origin_with_config` | Testseohelpersunit::get trusted canonical origin with config |
| 34 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_get_trusted_canonical_origin_rejects_crlf` | Testseohelpersunit::get trusted canonical origin rejects crlf |
| 35 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_get_trusted_canonical_origin_rejects_userinfo` | Testseohelpersunit::get trusted canonical origin rejects userinfo |
| 36 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_get_trusted_canonical_origin_rejects_non_http_scheme` | Testseohelpersunit::get trusted canonical origin rejects non http scheme |
| 37 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_build_sitemap_xml_basic_records` | Testseohelpersunit::build sitemap xml basic records |
| 38 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_build_sitemap_xml_object_records` | Testseohelpersunit::build sitemap xml object records |
| 39 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_build_sitemap_xml_deduplication` | Testseohelpersunit::build sitemap xml deduplication |
| 40 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_build_sitemap_xml_xml_character_escaping` | Testseohelpersunit::build sitemap xml xml character escaping |
| 41 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_build_robots_txt_format` | Testseohelpersunit::build robots txt format |
| 42 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_indexable_event_statuses_constant` | Testseohelpersunit::indexable event statuses constant |
| 43 | `tests/test_seo_sitemap_robots.py::TestSeoHelpersUnit::test_build_sitemap_xml_strictly_caps_at_max_urls` | Testseohelpersunit::build sitemap xml strictly caps at max urls |
| 44 | `tests/test_seo_sitemap_robots.py::TestSecurityAndPrivacyRegression::test_login_page_retains_noindex_nofollow` | Testsecurityandprivacyregression::login page retains noindex nofollow |
| 45 | `tests/test_seo_sitemap_robots.py::TestSecurityAndPrivacyRegression::test_register_page_retains_noindex_nofollow` | Testsecurityandprivacyregression::register page retains noindex nofollow |
| 46 | `tests/test_seo_sitemap_robots.py::TestSecurityAndPrivacyRegression::test_draft_event_remains_404_for_anonymous_user` | Testsecurityandprivacyregression::draft event remains 404 for anonymous user |
| 47 | `tests/test_seo_sitemap_robots.py::TestSecurityAndPrivacyRegression::test_cancelled_event_retains_noindex_follow` | Testsecurityandprivacyregression::cancelled event retains noindex follow |
| 48 | `tests/test_seo_sitemap_robots.py::TestSecurityAndPrivacyRegression::test_checkin_scanner_requires_auth` | Testsecurityandprivacyregression::checkin scanner requires auth |
| 49 | `tests/test_seo_sitemap_robots.py::TestSecurityAndPrivacyRegression::test_admin_dashboard_requires_auth` | Testsecurityandprivacyregression::admin dashboard requires auth |


## 11. `tests/test_tickets_and_quota.py` (6 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_tickets_and_quota.py::test_ticket_quota_limit` | Ticket quota limit |
| 02 | `tests/test_tickets_and_quota.py::test_checkin_anti_duplicate` | Checkin anti duplicate |
| 03 | `tests/test_tickets_and_quota.py::test_cancel_ticket_and_reclaim_quota` | Cancel ticket and reclaim quota |
| 04 | `tests/test_tickets_and_quota.py::test_re_register_after_cancel_or_pending` | Re register after cancel or pending |
| 05 | `tests/test_tickets_and_quota.py::test_auto_qr_generation_and_download` | Auto qr generation and download |
| 06 | `tests/test_tickets_and_quota.py::test_event_attendees_roster_and_quick_checkin` | Event attendees roster and quick checkin |


## 12. `tests/test_upgrade_requirements.py` (6 Tests)

| # | Test Node Identifier | Domain / Focus |
|---|---|---|
| 01 | `tests/test_upgrade_requirements.py::test_checkin_staff_permissions` | Checkin staff permissions |
| 02 | `tests/test_upgrade_requirements.py::test_schedule_time_validation_and_edit` | Schedule time validation and edit |
| 03 | `tests/test_upgrade_requirements.py::test_atomic_and_idempotent_checkin` | Atomic and idempotent checkin |
| 04 | `tests/test_upgrade_requirements.py::test_feedback_review_route` | Feedback review route |
| 05 | `tests/test_upgrade_requirements.py::test_pii_sanitization_and_email_placeholders` | Pii sanitization and email placeholders |
| 06 | `tests/test_upgrade_requirements.py::test_rag_step_8_response_validation` | Rag step 8 response validation |


---

## 3. Grand Total Verification

**Grand Total Collected**: 218 Tests across 12 files (100% Verified against `pytest --collect-only`).
